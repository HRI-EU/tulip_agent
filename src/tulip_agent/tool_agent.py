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
Agent variations with tool access as a baseline.
"""
import concurrent.futures
import json
import logging
from abc import ABC
from typing import Callable, Optional

from .base_agent import LlmAgent
from .constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from .function_analyzer import FunctionAnalyzer
from .prompts import SOLVE_WITH_TOOLS, TASK_DECOMPOSITION, TOOL_COT_PROMPT, TOOL_PROMPT


logger = logging.getLogger(__name__)


class ToolAgent(LlmAgent, ABC):
    def __init__(
        self,
        functions: list[Callable],
        instructions: str,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        api_interaction_limit: int = 100,
    ) -> None:
        super().__init__(
            instructions=instructions,
            model=model,
            temperature=temperature,
            api_interaction_limit=api_interaction_limit,
        )
        self.function_analyzer = FunctionAnalyzer()
        self.tools = {f.__name__: f for f in functions}
        self.tool_descriptions = [
            self.function_analyzer.analyze_function(f) for f in functions
        ]
        self.tool_timeout: int = 60
        self.tool_timeout_message: str = (
            "Error: The tool did not return a response within the specified timeout."
        )

    def run_with_tools(self):
        response = self._get_response(
            msgs=self.messages,
            tools=self.tool_descriptions,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        while tool_calls:
            self.messages.append(response_message)

            if self.api_interaction_counter >= self.api_interaction_limit:
                error_message = f"Error: Reached API interaction limit of {self.api_interaction_limit}."
                logger.error(
                    f"{self.__class__.__name__} returns response: {error_message}"
                )
                return error_message

            for tool_call in tool_calls:
                func_name = tool_call.function.name

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    try:
                        func_args = json.loads(tool_call.function.arguments)
                        future = executor.submit(self.tools[func_name], **func_args)
                        function_response = future.result(timeout=self.tool_timeout)
                    except json.decoder.JSONDecodeError as e:
                        logger.error(e)
                        generated_func_name = func_name
                        func_name = "invalid_tool_call"
                        tool_call.function.name = func_name
                        tool_call.function.arguments = "{}"
                        function_response = f"Error: Invalid arguments for {func_name} (previously {generated_func_name}): {e}"
                    except KeyError as e:
                        logger.error(
                            f"Invalid tool `{func_name}` resulting in error: {e}"
                        )
                        generated_func_name = func_name
                        func_name = "invalid_tool_call"
                        tool_call.function.name = func_name
                        tool_call.function.arguments = "{}"
                        function_response = f"Error: {generated_func_name} is not a valid tool. Use only the tools available."
                    except concurrent.futures.TimeoutError as e:
                        logger.error(
                            f"{type(e).__name__}: {func_name} did not return a result before timeout."
                        )
                        function_response = self.tool_timeout_message
                    except Exception as e:
                        logger.error(e)
                        function_response = (
                            f"Error: Invalid tool call for {func_name}: {e}"
                        )
                self.messages.append(
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
                msgs=self.messages,
                tools=self.tool_descriptions,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
        self.messages.append(response_message)
        logger.info(
            f"{self.__class__.__name__} returns response: {response_message.content}"
        )
        return response_message.content


class NaiveToolAgent(ToolAgent):
    def __init__(
        self,
        functions: list[Callable],
        instructions: Optional[str] = None,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        api_interaction_limit: int = 100,
    ) -> None:
        super().__init__(
            functions=functions,
            instructions=(
                TOOL_PROMPT + "\n\n" + instructions if instructions else TOOL_PROMPT
            ),
            model=model,
            temperature=temperature,
            api_interaction_limit=api_interaction_limit,
        )

    def query(
        self,
        prompt: str,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")
        self.messages.append({"role": "user", "content": prompt})
        return self.run_with_tools()


class CotToolAgent(ToolAgent):
    def __init__(
        self,
        functions: list[Callable],
        instructions: Optional[str] = None,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        api_interaction_limit: int = 100,
    ) -> None:
        super().__init__(
            instructions=(
                TOOL_COT_PROMPT + "\n\n" + instructions
                if instructions
                else TOOL_COT_PROMPT
            ),
            functions=functions,
            model=model,
            temperature=temperature,
            api_interaction_limit=api_interaction_limit,
        )

    def query(
        self,
        prompt: str,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")

        # Analyze user prompt
        self.messages.append(
            {
                "role": "user",
                "content": TASK_DECOMPOSITION.format(prompt=prompt),
            }
        )
        actions_response = self._get_response(
            msgs=self.messages,
        )
        actions_response_message = actions_response.choices[0].message
        self.messages.append(actions_response_message)
        logger.info(f"{actions_response_message=}")

        # Run with tools
        self.messages.append(
            {
                "role": "user",
                "content": SOLVE_WITH_TOOLS.format(
                    steps=actions_response_message.content
                ),
            }
        )
        return self.run_with_tools()
