#!/usr/bin/env python3
#
# Copyright (c) 2024, Honda Research Institute Europe GmbH
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""
TulipAgent ABC; uses a vector store as a tool library.
"""
import json
import logging
from abc import ABC
from typing import Optional

from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)

from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from tulip_agent.tool_library import ToolLibrary

from .base_agent import LlmAgent


logger = logging.getLogger(__name__)


class TulipAgent(LlmAgent, ABC):
    def __init__(
        self,
        instructions: str,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        api_interaction_limit: int = 100,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 3,
        search_similarity_threshold: float = None,
    ) -> None:
        super().__init__(
            instructions=instructions,
            model=model,
            temperature=temperature,
            api_interaction_limit=api_interaction_limit,
        )
        self.tool_library = tool_library
        self.top_k_functions = top_k_functions
        self.search_similarity_threshold = search_similarity_threshold

        self.search_tools_description = {
            "type": "function",
            "function": {
                "name": "search_tools",
                "description": "Search for tools in your tool library.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action_descriptions": {
                            "type": "array",
                            "items": {
                                "type": "string",
                            },
                            "description": (
                                "A list of textual descriptions for the actions you want to execute. "
                                "The description should be generic enough to find generic and reusable tools."
                            ),
                        },
                    },
                    "required": ["problem_description"],
                },
            },
        }

    def search_tools(
        self,
        action_descriptions: list[str],
        similarity_threshold: Optional[float] = None,
    ) -> list[tuple[str, list]]:
        json_res = {}
        tools = []
        for action_description in action_descriptions:
            if action_description in json_res:
                tools.append((action_description, json_res[action_description]))
                continue
            res = self.tool_library.search(
                problem_description=action_description,
                top_k=self.top_k_functions,
                similarity_threshold=similarity_threshold,
            )["documents"]
            if res:
                json_res_ = [json.loads(e) for e in res[0]]
                logger.info(
                    f"Functions for `{action_description}`: {json.dumps(json_res_)}"
                )
                json_res[action_description] = json_res_
                tools.append((action_description, json_res_))
        return tools

    def execute_search_tool_call(
        self,
        tool_call: ChatCompletionMessageToolCall,
        track_history: bool,
    ) -> list[tuple[str, list]]:
        func = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        assert func == "search_tools", f"Unexpected tool call: {func}"

        # search tulip for function with args
        logger.info(f"Tool search for: {str(args)}")
        tasks_and_tools = self.search_tools(
            **args, similarity_threshold=self.search_similarity_threshold
        )
        logger.info(f"Tools found: {str(tasks_and_tools)}")
        # TODO: add details to feedback message - task: suitable tools
        if track_history:
            self.messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": func,
                    "content": "Successfully provided suitable tools.",
                }
            )
        return tasks_and_tools

    def run_with_tools(
        self,
        tools: list[dict],
        messages: Optional[list] = None,
    ) -> str:
        if messages is None:
            messages = self.messages
        response = self._get_response(
            msgs=messages,
            tools=tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        while tool_calls:
            messages.append(response_message)

            if self.api_interaction_counter >= self.api_interaction_limit:
                error_message = f"Error: Reached API interaction limit of {self.api_interaction_limit}."
                logger.warning(f"{self.__class__.__name__}: {error_message}")
                return error_message

            for tool_call in tool_calls:
                func_name = tool_call.function.name
                try:
                    func_args = json.loads(tool_call.function.arguments)
                    function_response, error = self.tool_library.execute(
                        tool_id=func_name, arguments=func_args
                    )
                    if error:
                        func_name = "invalid_tool_call"
                        tool_call.function.name = func_name
                        tool_call.function.arguments = "{}"
                except json.decoder.JSONDecodeError as e:
                    logger.error(e)
                    generated_func_name = func_name
                    func_name = "invalid_tool_call"
                    tool_call.function.name = func_name
                    tool_call.function.arguments = "{}"
                    function_response = (
                        f"Error: Invalid arguments for {func_name} "
                        f"(previously {generated_func_name}): {e}"
                    )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": str(function_response),
                    }
                )
                logger.info(
                    (
                        f"Function {func_name} returned `{str(function_response)}` "
                        f"for arguments {tool_call.function.arguments}."
                    )
                )

            response = self._get_response(
                msgs=messages,
                tools=tools,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
        messages.append(response_message)
        return response_message.content