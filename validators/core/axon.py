import os
import uuid
import copy
import json
import time
import asyncio
import inspect
import uvicorn
import argparse
import traceback
import threading
import bittensor
import contextlib

from inspect import signature, Signature, Parameter
from fastapi.responses import JSONResponse
from substrateinterface import Keypair
from fastapi import FastAPI, APIRouter, Request, Response, Depends
from starlette.responses import Response
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from typing import List, Optional, Tuple, Callable, Any, Dict

from bittensor.errors import (
    InvalidRequestNameError,
    SynapseDendriteNoneException,
    SynapseParsingError,
    UnknownSynapseError,
    NotVerifiedException,
    BlacklistedException,
    PriorityException,
    RunException,
    PostProcessException,
    InternalServerError,
)
from bittensor.threadpool import PriorityThreadPoolExecutor
import bittensor
import bittensor as bt
from substrateinterface import Keypair
from bittensor.errors import SynapseDendriteNoneException
from cursor.app.core.config import config

class CortexAxon(bt.axon):
    def __init__(self,
                 wallet: Optional["bittensor.wallet"] = None,
                 config: Optional["bittensor.config"] = None,
                 port: Optional[int] = None,
                 ip: Optional[str] = None,
                 external_ip: Optional[str] = None,
                 external_port: Optional[int] = None,
                 max_workers: Optional[int] = None,
                 ):
        super().__init__(wallet, config, port, ip, external_ip, external_port, max_workers)
        self.app.add_middleware(CortexAxonMiddleware, axon=self)

    def default_verify(self, synapse: bittensor.Synapse):
        if synapse.dendrite is not None:
            keypair = Keypair(ss58_address=synapse.dendrite.hotkey)

            # Build the signature messages.
            message = f"{synapse.dendrite.nonce}.{synapse.dendrite.hotkey}.{self.wallet.hotkey.ss58_address}.{synapse.dendrite.uuid}.{synapse.computed_body_hash}"

            # Build the unique endpoint key.
            endpoint_key = f"{synapse.dendrite.hotkey}:{synapse.dendrite.uuid}"

            if not keypair.verify(message, synapse.dendrite.signature):
                raise Exception(
                    f"Signature mismatch with {message} and {synapse.dendrite.signature}"
                )

            # Success
            self.nonces[endpoint_key] = synapse.dendrite.nonce  # type: ignore
        else:
            raise SynapseDendriteNoneException()


class CortexAxonMiddleware(BaseHTTPMiddleware):
    """
    The `AxonMiddleware` class is a key component in the Axon server, responsible for processing all incoming requests.

    It handles the essential tasks of verifying requests, executing blacklist checks,
    running priority functions, and managing the logging of messages and errors. Additionally, the class
    is responsible for updating the headers of the response and executing the requested functions.

    This middleware acts as an intermediary layer in request handling, ensuring that each request is
    processed according to the defined rules and protocols of the Bittensor network. It plays a pivotal
    role in maintaining the integrity and security of the network communication.

    Args:
        app (FastAPI): An instance of the FastAPI application to which this middleware is attached.
        axon (bittensor.axon): The Axon instance that will process the requests.

    The middleware operates by intercepting incoming requests, performing necessary preprocessing
    (like verification and priority assessment), executing the request through the Axon's endpoints, and
    then handling any postprocessing steps such as response header updating and logging.
    """

    def __init__(self, app: "AxonMiddleware", axon: "bittensor.axon"):
        """
        Initialize the AxonMiddleware class.

        Args:
        app (object): An instance of the application where the middleware processor is used.
        axon (object): The axon instance used to process the requests.
        """
        super().__init__(app)
        self.axon = axon

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Asynchronously processes incoming HTTP requests and returns the corresponding responses. This
        method acts as the central processing unit of the AxonMiddleware, handling each step in the
        request lifecycle.

        Args:
            request (Request): The incoming HTTP request to be processed.
            call_next (RequestResponseEndpoint): A callable that processes the request and returns a response.

        Returns:
            Response: The HTTP response generated after processing the request.

        This method performs several key functions:

        1. Request Preprocessing: Sets up Synapse object from request headers and fills necessary information.
        2. Logging: Logs the start of request processing.
        3. Blacklist Checking: Verifies if the request is blacklisted.
        4. Request Verification: Ensures the authenticity and integrity of the request.
        5. Priority Assessment: Evaluates and assigns priority to the request.
        6. Request Execution: Calls the next function in the middleware chain to process the request.
        7. Response Postprocessing: Updates response headers and logs the end of the request processing.

        The method also handles exceptions and errors that might occur during each stage, ensuring that
        appropriate responses are returned to the client.
        """
        # Records the start time of the request processing.
        start_time = time.time()

        if "v1/chat/completions" in request.url.path:
            if request.method == "OPTIONS":
                return await call_next(request)
            try:
                api_key = request.headers.get("Authorization").split(" ")[1]
                if not api_key or api_key != config.api_key:
                    return JSONResponse(
                        {"detail": "Invalid or missing API Key"}, status_code=401
                    )
                return await call_next(request)
            except Exception:
                return JSONResponse(
                    {"detail": "Invalid or missing API Key"}, status_code=401
                )

        try:
            # Set up the synapse from its headers.
            synapse: bittensor.Synapse = await self.preprocess(request)

            # Logs the start of the request processing
            if synapse.dendrite is not None:
                bittensor.logging.trace(
                    f"axon     | <-- | {request.headers.get('content-length', -1)} B | {synapse.name} | {synapse.dendrite.hotkey} | {synapse.dendrite.ip}:{synapse.dendrite.port} | 200 | Success "
                )
            else:
                bittensor.logging.trace(
                    f"axon     | <-- | {request.headers.get('content-length', -1)} B | {synapse.name} | None | None | 200 | Success "
                )

            # Call the blacklist function
            await self.blacklist(synapse)

            # Call verify and return the verified request
            await self.verify(synapse)

            # Call the priority function
            await self.priority(synapse)

            # Call the run function
            response = await self.run(synapse, call_next, request)

            # Call the postprocess function
            response = await self.postprocess(synapse, response, start_time)

        # Handle errors related to preprocess.
        except InvalidRequestNameError as e:
            if "synapse" not in locals():
                synapse: bittensor.Synapse = bittensor.Synapse()  # type: ignore
            log_and_handle_error(synapse, e, 400, start_time)
            response = create_error_response(synapse)

        except SynapseParsingError as e:
            if "synapse" not in locals():
                synapse = bittensor.Synapse()
            log_and_handle_error(synapse, e, 400, start_time)
            response = create_error_response(synapse)

        except UnknownSynapseError as e:
            if "synapse" not in locals():
                synapse = bittensor.Synapse()
            log_and_handle_error(synapse, e, 404, start_time)
            response = create_error_response(synapse)

        # Handle errors related to verify.
        except NotVerifiedException as e:
            log_and_handle_error(synapse, e, 401, start_time)
            response = create_error_response(synapse)

        # Handle errors related to blacklist.
        except BlacklistedException as e:
            log_and_handle_error(synapse, e, 403, start_time)
            response = create_error_response(synapse)

        # Handle errors related to priority.
        except PriorityException as e:
            log_and_handle_error(synapse, e, 503, start_time)
            response = create_error_response(synapse)

        # Handle errors related to run.
        except RunException as e:
            log_and_handle_error(synapse, e, 500, start_time)
            response = create_error_response(synapse)

        # Handle errors related to postprocess.
        except PostProcessException as e:
            log_and_handle_error(synapse, e, 500, start_time)
            response = create_error_response(synapse)

        # Handle all other errors.
        except Exception as e:
            log_and_handle_error(synapse, InternalServerError(str(e)), 500, start_time)
            response = create_error_response(synapse)

        # Logs the end of request processing and returns the response
        finally:
            # Log the details of the processed synapse, including total size, name, hotkey, IP, port,
            # status code, and status message, using the debug level of the logger.
            if synapse.dendrite is not None and synapse.axon is not None:
                bittensor.logging.trace(
                    f"axon     | --> | {response.headers.get('content-length', -1)} B | {synapse.name} | {synapse.dendrite.hotkey} | {synapse.dendrite.ip}:{synapse.dendrite.port}  | {synapse.axon.status_code} | {synapse.axon.status_message}"
                )
            elif synapse.axon is not None:
                bittensor.logging.trace(
                    f"axon     | --> | {response.headers.get('content-length', -1)} B | {synapse.name} | None | None | {synapse.axon.status_code} | {synapse.axon.status_message}"
                )
            else:
                bittensor.logging.trace(
                    f"axon     | --> | {response.headers.get('content-length', -1)} B | {synapse.name} | None | None | 200 | Success "
                )

            # Return the response to the requester.
            return response

    async def preprocess(self, request: Request) -> bittensor.Synapse:
        """
        Performs the initial processing of the incoming request. This method is responsible for
        extracting relevant information from the request and setting up the Synapse object, which
        represents the state and context of the request within the Axon server.

        Args:
            request (Request): The incoming request to be preprocessed.

        Returns:
            bittensor.Synapse: The Synapse object representing the preprocessed state of the request.

        The preprocessing involves:

        1. Extracting the request name from the URL path.
        2. Creating a Synapse instance from the request headers using the appropriate class type.
        3. Filling in the Axon and Dendrite information into the Synapse object.
        4. Signing the Synapse from the Axon side using the wallet hotkey.

        This method sets the foundation for the subsequent steps in the request handling process,
        ensuring that all necessary information is encapsulated within the Synapse object.
        """
        # Extracts the request name from the URL path.
        try:
            request_name = request.url.path.split("/")[1]
        except:
            raise InvalidRequestNameError(
                f"Improperly formatted request. Could not parser request {request.url.path}."
            )

        # Creates a synapse instance from the headers using the appropriate forward class type
        # based on the request name obtained from the URL path.
        request_synapse = self.axon.forward_class_types.get(request_name)
        if request_synapse is None:
            raise UnknownSynapseError(
                f"Synapse name '{request_name}' not found. Available synapses {list(self.axon.forward_class_types.keys())}"
            )

        try:
            synapse = request_synapse.from_headers(request.headers)  # type: ignore
        except Exception as e:
            raise SynapseParsingError(
                f"Improperly formatted request. Could not parse headers {request.headers} into synapse of type {request_name}."
            )
        synapse.name = request_name

        # Fills the local axon information into the synapse.
        synapse.axon.__dict__.update(
            {
                "version": str(bittensor.__version_as_int__),
                "uuid": str(self.axon.uuid),
                "nonce": f"{time.monotonic_ns()}",
                "status_message": "Success",
                "status_code": "100",
            }
        )

        # Fills the dendrite information into the synapse.
        synapse.dendrite.__dict__.update(
            {"port": str(request.client.port), "ip": str(request.client.host)}  # type: ignore
        )

        # Signs the synapse from the axon side using the wallet hotkey.
        message = f"{synapse.axon.nonce}.{synapse.dendrite.hotkey}.{synapse.axon.hotkey}.{synapse.axon.uuid}"
        synapse.axon.signature = f"0x{self.axon.wallet.hotkey.sign(message).hex()}"

        # Return the setup synapse.
        return synapse

    async def verify(self, synapse: bittensor.Synapse):
        """
        Verifies the authenticity and integrity of the request. This method ensures that the incoming
        request meets the predefined security and validation criteria.

        Args:
            synapse (bittensor.Synapse): The Synapse object representing the request.

        Raises:
            Exception: If the verification process fails due to unmet criteria or security concerns.

        The verification process involves:

        1. Retrieving the specific verification function for the request's Synapse type.
        2. Executing the verification function and handling any exceptions that arise.

        Successful verification allows the request to proceed further in the processing pipeline, while
        failure results in an appropriate exception being raised.
        """
        # Start of the verification process. Verification is the process where we ensure that
        # the incoming request is from a trusted source or fulfills certain requirements.
        # We get a specific verification function from 'verify_fns' dictionary that corresponds
        # to our request's name. Each request name (synapse name) has its unique verification function.
        verify_fn = (
            self.axon.verify_fns.get(synapse.name) if synapse.name is not None else None
        )

        # If a verification function exists for the request's name
        if verify_fn:
            try:
                # We attempt to run the verification function using the synapse instance
                # created from the request. If this function runs without throwing an exception,
                # it means that the verification was successful.
                (
                    await verify_fn(synapse)
                    if inspect.iscoroutinefunction(verify_fn)
                    else verify_fn(synapse)
                )
            except Exception as e:
                # If there was an exception during the verification process, we log that
                # there was a verification exception.
                bittensor.logging.trace(f"Verify exception {str(e)}")

                # Check if the synapse.axon object exists
                if synapse.axon is not None:
                    # We set the status code of the synapse to "401" which denotes an unauthorized access.
                    synapse.axon.status_code = 401
                else:
                    # If the synapse.axon object doesn't exist, raise an exception.
                    raise Exception("Synapse.axon object is None")

                # We raise an exception to stop the process and return the error to the requester.
                # The error message includes the original exception message.
                raise NotVerifiedException(f"Not Verified with error: {str(e)}")

    async def blacklist(self, synapse: bittensor.Synapse):
        """
        Checks if the request should be blacklisted. This method ensures that requests from disallowed
        sources or with malicious intent are blocked from processing. This can be extremely useful for
        preventing spam or other forms of abuse. The blacklist is a list of keys or identifiers that
        are prohibited from accessing certain resources.

        Args:
            synapse (bittensor.Synapse): The Synapse object representing the request.

        Raises:
            Exception: If the request is found in the blacklist.

        The blacklist check involves:

        1. Retrieving the blacklist checking function for the request's Synapse type.
        2. Executing the check and handling the case where the request is blacklisted.

        If a request is blacklisted, it is blocked, and an exception is raised to halt further processing.
        """
        # A blacklist is a list of keys or identifiers
        # that are prohibited from accessing certain resources.
        # We retrieve the blacklist checking function from the 'blacklist_fns' dictionary
        # that corresponds to the request's name (synapse name).
        blacklist_fn = (
            self.axon.blacklist_fns.get(synapse.name)
            if synapse.name is not None
            else None
        )

        # If a blacklist checking function exists for the request's name
        if blacklist_fn:
            # We execute the blacklist checking function using the synapse instance as input.
            # If the function returns True, it means that the key or identifier is blacklisted.
            blacklisted, reason = (
                await blacklist_fn(synapse)
                if inspect.iscoroutinefunction(blacklist_fn)
                else blacklist_fn(synapse)
            )
            if blacklisted:
                # We log that the key or identifier is blacklisted.
                bittensor.logging.trace(f"Blacklisted: {blacklisted}, {reason}")

                # Check if the synapse.axon object exists
                if synapse.axon is not None:
                    # We set the status code of the synapse to "403" which indicates a forbidden access.
                    synapse.axon.status_code = 403
                else:
                    # If the synapse.axon object doesn't exist, raise an exception.
                    raise Exception("Synapse.axon object is None")

                # We raise an exception to halt the process and return the error message to the requester.
                raise BlacklistedException(f"Forbidden. Key is blacklisted: {reason}.")

    async def priority(self, synapse: bittensor.Synapse):
        """
        Executes the priority function for the request. This method assesses and assigns a priority
        level to the request, determining its urgency and importance in the processing queue.

        Args:
            synapse (bittensor.Synapse): The Synapse object representing the request.

        Raises:
            Exception: If the priority assessment process encounters issues, such as timeouts.

        The priority function plays a crucial role in managing the processing load and ensuring that
        critical requests are handled promptly.
        """
        # Retrieve the priority function from the 'priority_fns' dictionary that corresponds
        # to the request's name (synapse name).
        priority_fn = self.axon.priority_fns.get(str(synapse.name), None)

        async def submit_task(
                executor: PriorityThreadPoolExecutor, priority: float
        ) -> Tuple[float, Any]:
            """
            Submits the given priority function to the specified executor for asynchronous execution.
            The function will run in the provided executor and return the priority value along with the result.

            Args:
                executor: The executor in which the priority function will be run.
                priority: The priority function to be executed.

            Returns:
                tuple: A tuple containing the priority value and the result of the priority function execution.
            """
            loop = asyncio.get_event_loop()
            future = loop.run_in_executor(executor, lambda: priority)
            result = await future
            return priority, result

        # If a priority function exists for the request's name
        if priority_fn:
            try:
                # Execute the priority function and get the priority value.
                priority = (
                    await priority_fn(synapse)
                    if inspect.iscoroutinefunction(priority_fn)
                    else priority_fn(synapse)
                )

                # Submit the task to the thread pool for execution with the given priority.
                # The submit_task function will handle the execution and return the result.
                _, result = await submit_task(self.axon.thread_pool, priority)

            except TimeoutError as e:
                # If the execution of the priority function exceeds the timeout,
                # it raises an exception to handle the timeout error.
                bittensor.logging.trace(f"TimeoutError: {str(e)}")

                # Set the status code of the synapse to 408 which indicates a timeout error.
                if synapse.axon is not None:
                    synapse.axon.status_code = 408

                # Raise an exception to stop the process and return an appropriate error message to the requester.
                raise PriorityException(f"Response timeout after: {synapse.timeout}s")

    async def run(
            self,
            synapse: bittensor.Synapse,
            call_next: RequestResponseEndpoint,
            request: Request,
    ) -> Response:
        """
        Executes the requested function as part of the request processing pipeline. This method calls
        the next function in the middleware chain to process the request and generate a response.

        Args:
            synapse (bittensor.Synapse): The Synapse object representing the request.
            call_next (RequestResponseEndpoint): The next function in the middleware chain to process requests.
            request (Request): The original HTTP request.

        Returns:
            Response: The HTTP response generated by processing the request.

        This method is a critical part of the request lifecycle, where the actual processing of the
        request takes place, leading to the generation of a response.
        """
        try:
            # The requested function is executed by calling the 'call_next' function,
            # passing the original request as an argument. This function processes the request
            # and returns the response.
            response = await call_next(request)

        except Exception as e:
            # If an exception occurs during the execution of the requested function,
            # it is caught and handled here.

            # Log the exception for debugging purposes.
            bittensor.logging.trace(f"Run exception: {str(e)}")

            # Set the status code of the synapse to "500" which indicates an internal server error.
            if synapse.axon is not None:
                synapse.axon.status_code = 500

            # Raise an exception to stop the process and return an appropriate error message to the requester.
            raise RunException(f"Internal server error with error: {str(e)}")

        # Return the starlet response
        return response

    async def postprocess(
            self, synapse: bittensor.Synapse, response: Response, start_time: float
    ) -> Response:
        """
        Performs the final processing on the response before sending it back to the client. This method
        updates the response headers and logs the end of the request processing.

        Args:
            synapse (bittensor.Synapse): The Synapse object representing the request.
            response (Response): The response generated by processing the request.
            start_time (float): The timestamp when the request processing started.

        Returns:
            Response: The final HTTP response, with updated headers, ready to be sent back to the client.

        Postprocessing is the last step in the request handling process, ensuring that the response is
        properly formatted and contains all necessary information.
        """
        # Set the status code of the synapse to "200" which indicates a successful response.
        if synapse.axon is not None:
            synapse.axon.status_code = 200

            # Set the status message of the synapse to "Success".
            synapse.axon.status_message = "Success"

        try:
            # Update the response headers with the headers from the synapse.
            updated_headers = synapse.to_headers()
            response.headers.update(updated_headers)
        except Exception as e:
            # If there is an exception during the response header update, we log the exception.
            raise PostProcessException(
                f"Error while parsing or updating response headers. Postprocess exception: {str(e)}."
            )

        # Calculate the processing time by subtracting the start time from the current time.
        synapse.axon.process_time = str(time.time() - start_time)  # type: ignore

        return response
