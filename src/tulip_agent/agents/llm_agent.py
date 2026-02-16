#!/usr/bin/env python3
#
#  Copyright (c) 2024-2025, Honda Research Institute Europe GmbH
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  SPDX-License-Identifier: BSD-3-Clause
#
#
"""
LLM agent ABC.
"""
import logging
import time
from abc import ABC, abstractmethod
from typing import Callable

from openai import AzureOpenAI, BadRequestError, OpenAI, OpenAIError
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from tulip_agent.client_setup import ModelServeMode, create_client
from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_REASONING_MODEL
from tulip_agent.tool import InternalTool, Tool
from tulip_agent.tool_execution import execute_tool_calls


logger = logging.getLogger(__name__)


class LlmAgent(ABC):
    def __init__(
        self,
        instructions: str,
        base_model: str | None,
        base_client: AzureOpenAI | OpenAI | None,
        reasoning_model: str | None,
        reasoning_client: AzureOpenAI | OpenAI | None,
        temperature: float | None,
        api_interaction_limit: int,
    ) -> None:
        self.reasoning_available = True if reasoning_model else False
        self.reasoning_only = reasoning_model and not base_model

        self.base_model = base_model or reasoning_model or BASE_LANGUAGE_MODEL
        self.base_client = (
            base_client or reasoning_client or create_client(ModelServeMode.OPENAI)
        )
        self.reasoning_model = reasoning_model or base_model or BASE_REASONING_MODEL
        self.reasoning_client = reasoning_client or self.base_client

        self.temperature = temperature
        self.instructions = instructions

        self.messages = []
        if self.instructions:
            self.messages.append({"role": "system", "content": self.instructions})

        self.api_interaction_limit = api_interaction_limit
        self.api_interaction_counter = 0
        self.max_retries = 5

        self.response: str | None = None

    def stop(self, message: str) -> str:
        """
        Stop and return a final message to the user.

        :param message: The message to return.
        :return: The final response to be given to the user.
        """
        self.response = message
        return "Done."

    def _create_stop_tool(
        self,
        analyze_function: Callable[[Callable], dict],
    ) -> InternalTool:
        return InternalTool(
            function_name=self.stop.__name__,
            definition=analyze_function(self.stop),
            function=self.stop,
        )

    def _get_response(
        self,
        msgs: list[dict[str, str]],
        tools: list = None,
        tool_choice: str = "auto",
        reasoning: bool = False,
        response_format: str = None,
    ):
        client = self.reasoning_client if reasoning else self.base_client
        reasoning = (
            True
            if self.reasoning_only
            else False if not self.reasoning_available else reasoning
        )

        self.api_interaction_counter += 1
        response, retries = None, 0

        while not response:
            params = {
                "model": self.reasoning_model if reasoning else self.base_model,
                "messages": msgs,
            }
            if tools:
                params["tools"] = tools
                params["tool_choice"] = tool_choice
            if response_format == "json":
                params["response_format"] = {"type": "json_object"}
            if not reasoning and not params["model"].startswith("gpt-5"):
                params["temperature"] = self.temperature
            try:
                response = client.chat.completions.create(**params)
            # Return error message for bad requests, e.g., repetitive inputs or context window exceeded
            except BadRequestError as e:
                logger.error(f"{type(e).__name__}: {e}")
                return ChatCompletion(
                    id="abort",
                    choices=[
                        Choice(
                            finish_reason="stop",
                            index=0,
                            message=ChatCompletionMessage(
                                content=f"{type(e).__name__}: {e}", role="assistant"
                            ),
                        )
                    ],
                    created=int(time.time()),
                    model=self.base_model,
                    object="chat.completion",
                )
            except OpenAIError as e:
                logger.error(f"{type(e).__name__}: {e}")
                retries += 1
                time.sleep(retries / 4)
                if retries >= self.max_retries:
                    raise e
        logger.info(
            f"Usage for {response.id} in tokens: "
            f"{response.usage.prompt_tokens} prompt and {response.usage.completion_tokens} completion."
        )
        return response

    @abstractmethod
    def query(
        self,
        prompt: str,
    ) -> str:
        """
        Query the agent.

        :param prompt: User prompt
        :return: User-oriented final response
        """
        raise NotImplementedError()

    def _run_tool_loop(
        self,
        tools: list[Tool],
        messages: list | None = None,
        execute_tool_calls_fn: Callable | None = None,
    ) -> str:
        if messages is None:
            messages = self.messages
        if execute_tool_calls_fn is None:
            execute_tool_calls_fn = execute_tool_calls

        response = self._get_response(
            msgs=messages,
            tools=[tool.definition for tool in tools],
            tool_choice="required",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        while self.response is None:
            if not tool_calls:
                error_message = "Invalid response - no tool calls."
                logger.error(
                    f"{self.__class__.__name__} returns response: {error_message}"
                )
                return error_message

            messages.append(response_message)

            if self.api_interaction_counter >= self.api_interaction_limit:
                error_message = f"Error: Reached API interaction limit of {self.api_interaction_limit}."
                logger.warning(f"{self.__class__.__name__}: {error_message}")
                return error_message

            execute_tool_calls_fn(
                tool_calls=tool_calls,
                messages=messages,
                tools={tool.unique_id: tool for tool in tools},
            )

            response = self._get_response(
                msgs=messages,
                tools=[tool.definition for tool in tools],
                tool_choice="required",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

        if self.response is None:
            raise RuntimeError("Tool loop ended without a final response.")
        return self.response
