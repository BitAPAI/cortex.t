import json
from typing import AsyncGenerator
import bittensor as bt
from cursor.app.models import ChatRequest
from cursor.app.core.protocol import StreamPrompting
from cursor.app.core.config import config
from cortext.dendrite import CortexDendrite
import traceback
from loguru import logger
import numpy as np

subtensor = bt.subtensor(network="finney")
meta = subtensor.metagraph(netuid=18)
logger.info("metagraph synched!")

# This needs to be your validator wallet that is running your subnet 18 validator
wallet = bt.wallet(name=config.wallet_name, hotkey=config.wallet_hotkey)
logger.info(f"wallet_name is {config.wallet_name}, hot_key is {config.wallet_hotkey}")
dendrite = CortexDendrite(wallet=wallet)
vali_uid = meta.hotkeys.index(wallet.hotkey.ss58_address)
# axon_to_use = meta.axons[vali_uid]
import threading
import time

top_incentive_axons = []
logger.info(f"top_incentive_axons: {top_incentive_axons}")

def update_top_incentive_axons():
    global top_incentive_axons
    while True:
        axons = meta.axons
        incentives = meta.I
        # Convert incentives to numpy array and get indices of top 50
        incentive_indices = np.argsort(np.array(incentives, dtype=np.float32))[-50:]
        logger.info(f"incentive_indices: {incentive_indices}")
        top_incentive_axons = [axons[int(i)] for i in incentive_indices]
        logger.info(f"top_incentive_axons: {top_incentive_axons}")
        time.sleep(600)  # Sleep for 10 minutes

def get_top_incentive_axons():
    global top_incentive_axons
    return top_incentive_axons

# Start background thread
thread = threading.Thread(target=update_top_incentive_axons, daemon=True)
thread.start()
import random

async def query_miner(chat_request: ChatRequest) -> AsyncGenerator[str, None]:
    try:
        synapse = StreamPrompting(**chat_request.dict())
        axon_to_use = random.choice(get_top_incentive_axons())
        logger.info("query_miner.synapse", synapse)
        resp = dendrite.call_stream(
            target_axon=axon_to_use,
            synapse=synapse,
            timeout=60
        )
        logger.info("query_miner.resp", resp)
        async for chunk in resp:
            logger.info("query_miner.chunk", chunk)
            if isinstance(chunk, str):
                obj = {"id":"chatcmpl-abc123","object":"chat.completion.chunk","choices":[{"delta":{"content":chunk},"index":0,"finish_reason":None}]}
                yield "data: " + json.dumps(obj) + "\n\n"
                logger.info(chunk, end='', flush=True)
            else:
                logger.info(f"\n\nFinal synapse: {chunk}\n")
        yield "[DONE]"
    except Exception as e:
        logger.info(f"Exception during query: {traceback.format_exc()}")
        yield "Exception ocurred."

async def query_miner_no_stream(chat_request: ChatRequest):
    try:
        synapse = StreamPrompting(**chat_request.dict())
        axon_to_use = random.choice(get_top_incentive_axons())
        resp = dendrite.call_stream(
            target_axon=axon_to_use,
            synapse=synapse,
            timeout=60
        )
        full_resp = ""
        async for chunk in resp:
            if isinstance(chunk, str):
                full_resp += chunk
                logger.info(chunk, end='', flush=True)
            else:
                logger.info(f"\n\nFinal synapse: {chunk}\n")
        return full_resp

    except Exception as e:
        logger.info(f"Exception during query: {traceback.format_exc()}")
        return ""