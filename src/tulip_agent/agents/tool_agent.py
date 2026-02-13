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
Tool agent ABC.
"""
import json
import logging
from abc import ABC
from typing import Callable

from openai import AzureOpenAI, OpenAI

from tulip_agent.agents.base_agent import LlmAgent
from tulip_agent.function_analyzer import FunctionAnalyzer
from tulip_agent.tool import InternalTool
from tulip_agent.tool_execution import Job, execute_tool_calls


logger = logging.getLogger(__name__)


class ToolAgent(LlmAgent, ABC):
    def __init__(
        self,
        functions: list[Callable],
        instructions: str,
        base_model: str | None,
        base_client: AzureOpenAI | OpenAI | None,
        reasoning_model: str | None,
        reasoning_client: AzureOpenAI | OpenAI | None,
        temperature: float | None,
        api_interaction_limit: int,
    ) -> None:
        super().__init__(
            instructions=instructions,
            base_model=base_model,
            base_client=base_client,
            reasoning_model=reasoning_model,
            reasoning_client=reasoning_client,
            temperature=temperature,
            api_interaction_limit=api_interaction_limit,
        )
        self.function_analyzer = FunctionAnalyzer()
        stop_tool = InternalTool(
            function_name=self.stop.__name__,
            definition=self.function_analyzer.analyze_function(self.stop),
            function=self.stop,
        )
        self.tools = {
            function.__name__: InternalTool(
                function_name=function.__name__,
                definition=self.function_analyzer.analyze_function(function),
                function=function,
                timeout=60.0,
                timeout_message="Error: The tool did not return a response within the specified timeout.",
            )
            for function in functions
        }
        self.tools["stop_tool"] = stop_tool
        self.response: str | None = None

    def stop(self, message: str) -> str:
        """
        Stop and return a final message to the user.

        :param message: The message to return.
        :return: The final response to be given to the user.
        """
        self.response = message
        return "Done."

    def run_with_tools(self):
        self.response = None
        response = self._get_response(
            msgs=self.messages,
            tools=[tool.definition for tool in self.tools],
            tool_choice="required",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        while not self.response:
            if not tool_calls:
                error_message = "Invalid response - no tool calls."
                logger.error(
                    f"{self.__class__.__name__} returns response: {error_message}"
                )
                return error_message

            self.messages.append(response_message)

            if self.api_interaction_counter >= self.api_interaction_limit:
                error_message = f"Error: Reached API interaction limit of {self.api_interaction_limit}."
                logger.error(
                    f"{self.__class__.__name__} returns response: {error_message}"
                )
                return error_message

            tool_messages = [{} for _ in tool_calls]
            valid_calls = []
            jobs = []

            for i, tool_call in enumerate(tool_calls):
                func_name = tool_call.function.name
                try:
                    func_args = json.loads(tool_call.function.arguments)
                except json.decoder.JSONDecodeError as e:
                    logger.error(e)
                    generated_func_name, func_name = func_name, "invalid_tool_call"
                    tool_call.function.name = func_name
                    tool_call.function.arguments = "{}"
                    function_response = f"Error: Invalid arguments for {func_name} (previously {generated_func_name}): {e}"
                    tool_messages[i] = {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": function_response,
                    }
                    continue

                if func_name not in self.tools:
                    logger.error(f"Invalid tool `{func_name}`.")
                    generated_func_name = func_name
                    func_name = "invalid_tool_call"
                    tool_call.function.name = func_name
                    tool_call.function.arguments = "{}"
                    function_response = f"Error: {generated_func_name} is not a valid tool. Use only the tools available."
                    tool_messages[i] = {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": function_response,
                    }
                    continue

                valid_calls.append((i, tool_call, func_name))
                jobs.append(
                    Job(
                        tool_call_id=tool_call.id,
                        tool=self.tools[func_name],
                        parameters=func_args,
                    )
                )

            execution_results = execute_tool_calls(jobs=jobs)
            for (i, tool_call, func_name), execution_result in zip(
                valid_calls, execution_results
            ):
                if execution_result.result.error:
                    logger.error(execution_result.result.error)
                    function_response = execution_result.result.error
                    func_name = "invalid_tool_call"
                    tool_call.function.name = func_name
                    tool_call.function.arguments = "{}"
                else:
                    function_response = execution_result.result.value

                tool_messages[i] = {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": func_name,
                    "content": str(function_response),
                }

            for tool_message, tool_call in zip(tool_messages, tool_calls):
                self.messages.append(tool_message)
                logger.info(
                    (
                        f"Function {tool_message['name']} returned `{tool_message['content']}` "
                        f"for arguments {tool_call.function.arguments}."
                    )
                )

            response = self._get_response(
                msgs=self.messages,
                tools=[tool.definition for tool in self.tools],
                tool_choice="required",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
        return self.response
