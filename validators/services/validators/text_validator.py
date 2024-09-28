import random
import bittensor as bt
from typing import AsyncIterator

from cortext.reward import model
from cortext import constants
import cortext.reward
from validators.services.validators.base_validator import BaseValidator
from validators.utils import error_handler
from typing import Optional
from cortext.protocol import StreamPrompting
from cortext.utils import (call_anthropic_bedrock, call_bedrock, call_anthropic, call_gemini,
                           call_groq, call_openai, get_question)
from validators.utils import save_answer_to_cache


class TextValidator(BaseValidator):
    def __init__(self, config, provider: str = None, model: str = None, metagraph=None):
        super().__init__(config, metagraph)
        self.streaming = True
        self.query_type = "text"
        self.metagraph = metagraph
        self.model = model or constants.TEXT_MODEL
        self.max_tokens = constants.TEXT_MAX_TOKENS
        self.temperature = constants.TEXT_TEMPERATURE
        self.weight = constants.TEXT_WEIGHT
        self.top_p = constants.TEXT_TOP_P
        self.top_k = constants.TEXT_TOP_K
        self.provider = provider or constants.TEXT_PROVIDER

        self.wandb_data = {
            "modality": "text",
            "prompts": {},
            "responses": {},
            "scores": {},
            "timestamps": {},
        }

    async def organic(self, metagraph, query: dict[str, list[dict[str, str]]]) -> AsyncIterator[tuple[int, str]]:
        for uid, messages in query.items():
            syn = StreamPrompting(
                messages=messages,
                model=self.model,
                seed=self.seed,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                provider=self.provider,
                top_p=self.top_p,
                top_k=self.top_k,
            )
            bt.logging.info(
                f"Sending {syn.model} {self.query_type} request to uid: {uid}, "
                f"timeout {self.timeout}: {syn.messages[0]['content']}"
            )

            # self.wandb_data["prompts"][uid] = messages
            responses = await self.dendrite(
                metagraph.axons[uid],
                syn,
                deserialize=False,
                timeout=self.timeout,
                streaming=self.streaming,
            )

            async for resp in responses:
                if not isinstance(resp, str):
                    continue

                bt.logging.trace(resp)
                yield uid, resp

    async def get_question(self, miner_cnt=1):
        is_vision_model = self.model in constants.VISION_MODELS
        question = await get_question("text", miner_cnt, is_vision_model)
        return question

    async def create_query(self, uid, provider=None, model=None) -> bt.Synapse:
        question = await self.get_question()
        prompt = question.get("prompt")
        image = question.get("image")
        if image:
            messages = [{'role': 'user', 'content': prompt, "image": image}]
        else:
            messages = [{'role': 'user', 'content': prompt}]

        syn = StreamPrompting(messages=messages, model=model, seed=self.seed, max_tokens=self.max_tokens,
                              temperature=self.temperature, provider=provider, top_p=self.top_p,
                              top_k=self.top_k)
        return syn

    def select_random_provider_and_model(self):
        # AnthropicBedrock should only be used if a validators' anthropic account doesn't work
        providers = ["OpenAI"] * 60 + ["AnthropicBedrock"] * 0 + ["Gemini"] * 2 + ["Anthropic"] * 25 + [
            "Groq"] * 20 + ["Bedrock"] * 2
        self.provider = random.choice(providers)

        model_to_weights = constants.TEXT_VALI_MODELS_WEIGHTS[self.provider]
        self.model = random.choices(list(model_to_weights.keys()),
                                    weights=list(model_to_weights.values()), k=1)[0]

    def get_provider_to_models(self):
        provider_models = []
        for provider in constants.TEXT_VALI_MODELS_WEIGHTS:
            models = constants.TEXT_VALI_MODELS_WEIGHTS.get(provider).keys()
            for model_ in models:
                provider_models.append((provider, model_))
        return provider_models

    @error_handler
    async def build_wandb_data(self, uid_to_score, responses):
        for uid, _ in self.uid_to_questions.items():
            prompt = self.uid_to_questions[uid]
            self.wandb_data["scores"][uid] = uid_to_score[uid]
            self.wandb_data["prompts"][uid] = prompt
        for uid, response in responses:
            self.wandb_data["responses"][uid] = response
        return self.wandb_data

    async def call_api(self, prompt: str, image_url: Optional[str], query_syn: StreamPrompting) -> str:
        provider = query_syn.provider
        self.model = query_syn.model
        if provider == "OpenAI":
            return await call_openai(
                [{"role": "user", "content": prompt, "image": image_url}], self.temperature, self.model, self.seed,
                self.max_tokens
            )
        elif provider == "AnthropicBedrock":
            return await call_anthropic_bedrock(prompt, self.temperature, self.model, self.max_tokens, self.top_p,
                                                self.top_k)
        elif provider == "Gemini":
            return await call_gemini(prompt, self.temperature, self.model, self.max_tokens, self.top_p, self.top_k)
        elif provider == "Anthropic":
            return await call_anthropic(
                [{"role": "user", "content": prompt, "image": image_url}],
                self.temperature,
                self.model,
                self.max_tokens,
                self.top_p,
                self.top_k,
            )
        elif provider == "Groq":
            return await call_groq(
                [{"role": "user", "content": prompt}],
                self.temperature,
                self.model,
                self.max_tokens,
                self.top_p,
                self.seed,
            )
        elif provider == "Bedrock":
            return await call_bedrock(
                [{"role": "user", "content": prompt, "image": image_url}],
                self.temperature,
                self.model,
                self.max_tokens,
                self.top_p,
                self.seed,
            )
        else:
            bt.logging.error(f"provider {provider} not found")

    @save_answer_to_cache
    async def get_answer_task(self, uid: int, query_syn: StreamPrompting, response):
        prompt = query_syn.messages[0].get("content")
        image_url = query_syn.messages[0].get("image")
        answer = await self.call_api(prompt, image_url, query_syn)
        return answer

    async def get_scoring_task(self, uid, answer, response):
        response_str, _ = response
        return await cortext.reward.api_score(answer, response_str, self.weight, self.temperature, self.provider)

    @classmethod
    def get_task_type(cls):
        return StreamPrompting.__name__

    @staticmethod
    def get_synapse_from_json(data):
        synapse = StreamPrompting.parse_raw(data)
        return synapse

