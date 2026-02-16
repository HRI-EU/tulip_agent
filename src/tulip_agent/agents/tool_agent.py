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
import logging
from abc import ABC
from typing import Callable

from openai import AzureOpenAI, OpenAI

from tulip_agent.agents.base_agent import LlmAgent
from tulip_agent.function_analyzer import FunctionAnalyzer
from tulip_agent.tool import ExternalTool, InternalTool, Tool


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
        self.tools: list[Tool] = [
            ExternalTool(
                function_name=function.__name__,
                definition=self.function_analyzer.analyze_function(function),
                function=function,
                timeout=60.0,
                timeout_message="The tool did not return a response within the specified timeout.",
            )
            for function in functions
        ]
        self.tools.append(stop_tool)

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
        return self._run_tool_loop(tools=self.tools)
