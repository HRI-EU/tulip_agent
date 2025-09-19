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
NaiveTulipAgent variant.
"""

import logging
from typing import Optional

from openai import AzureOpenAI, OpenAI

from tulip_agent.agents.prompts import TOOL_PROMPT
from tulip_agent.agents.tulip_agent import TulipAgent
from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from tulip_agent.tool import Tool
from tulip_agent.tool_library import ToolLibrary


logger = logging.getLogger(__name__)


class NaiveTulipAgent(TulipAgent):
    def __init__(
        self,
        tool_library: ToolLibrary,
        instructions: str | None = None,
        base_model: str | None = None,
        base_client: AzureOpenAI | OpenAI | None = None,
        reasoning_model: str | None = None,
        reasoning_client: AzureOpenAI | OpenAI | None = None,
        temperature: float | None = None,
        api_interaction_limit: int = 100,
        default_tools: Optional[list[Tool]] = None,
        top_k_functions: int = 10,
        search_similarity_threshold: float = None,
    ) -> None:
        if base_model is None and reasoning_model is None:
            base_model = BASE_LANGUAGE_MODEL
            temperature = BASE_TEMPERATURE
        super().__init__(
            instructions=(instructions or TOOL_PROMPT),
            tool_library=tool_library,
            base_model=base_model,
            base_client=base_client,
            reasoning_model=reasoning_model,
            reasoning_client=reasoning_client,
            temperature=temperature,
            api_interaction_limit=api_interaction_limit,
            default_tools=default_tools,
            top_k_functions=top_k_functions,
            search_similarity_threshold=search_similarity_threshold,
        )

    def query(
        self,
        prompt: str,
        tool_search_retries: int = 3,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")

        self.messages.append(
            {
                "role": "user",
                "content": f"Search for appropriate tools for reacting to the following user request: {prompt}.",
            }
        )
        tools, retries = None, 0
        while not tools:
            function_response = self._get_response(
                msgs=self.messages,
                tools=[self.search_tools_description],
                tool_choice={"type": "function", "function": {"name": "search_tools"}},
            )
            response_message = function_response.choices[0].message
            self.messages.append(response_message)
            tool_calls = response_message.tool_calls

            if not tool_calls:
                logger.info("Tool search invalid: No tool search conducted. Retrying.")
                self.messages.append(
                    {
                        "role": "user",
                        "content": "Error: You MUST search for tools by returning a single call to `search_tools`.",
                    }
                )
            # More than one tool call - several searches should be combined in one call
            elif (lntc := len(tool_calls)) > 1:
                logger.info(
                    f"Tool search invalid: Returned {lntc} instead of 1 search call. Retrying."
                )
                for tool_call in tool_calls:
                    self.messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "search_tools",
                            "content": "Error: Invalid number of tool calls; return a single call to `search_tools`.",
                        }
                    )
            # Try running search for tools from tool call
            else:
                try:
                    tools_ = self.execute_search_tool_call(
                        tool_call=tool_calls[0], track_history=True
                    )
                    tools = [tool for partial in tools_ for tool in partial[1]]
                    if tools:
                        break
                    else:
                        self.messages.append(
                            {
                                "tool_call_id": tool_calls[0].id,
                                "role": "tool",
                                "name": "search_tools",
                                "content": "Did not find any tools. Retry by paraphrasing.",
                            }
                        )
                except Exception as e:
                    logger.info(
                        f"Invalid tool call for `search_tools`: `{e}`. Retrying."
                    )
                    self.messages.append(
                        {
                            "tool_call_id": tool_calls[0].id,
                            "role": "tool",
                            "name": "search_tools",
                            "content": f"Error: Invalid tool call for `search_tools`: {e}",
                        }
                    )
            retries += 1
            if retries >= tool_search_retries:
                error_message = (
                    f"Aborting: Searching for tools failed {tool_search_retries} times."
                )
                logger.error(error_message)
                return error_message

        # Run with tools
        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        response = self.run_with_tools(tools=tools)
        logger.info(f"{self.__class__.__name__} returns response: {response}")
        self.api_interaction_counter = 0
        return response
