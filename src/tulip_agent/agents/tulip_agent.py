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
import ast
import json
import logging
import os
import subprocess
from abc import ABC
from typing import Optional

from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)

from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from tulip_agent.prompts import TECH_LEAD
from tulip_agent.tool import Tool
from tulip_agent.tool_library import ToolLibrary

from .base_agent import LlmAgent, ModelServeMode


logger = logging.getLogger(__name__)


class TulipAgent(LlmAgent, ABC):
    def __init__(
        self,
        instructions: str,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        model_serve_mode: ModelServeMode = ModelServeMode.OPENAI,
        api_interaction_limit: int = 100,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 3,
        search_similarity_threshold: float = None,
    ) -> None:
        super().__init__(
            instructions=instructions,
            model=model,
            temperature=temperature,
            model_serve_mode=model_serve_mode,
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
    ) -> list[tuple[str, list[Tool]]]:
        """Find suitable tools for each action description."""
        tool_lookup = {}
        actions_with_tools = []
        for action_description in action_descriptions:
            if action_description in tool_lookup:
                actions_with_tools.append(
                    (action_description, tool_lookup[action_description])
                )
                continue
            tools = self.tool_library.search(
                problem_description=action_description,
                top_k=self.top_k_functions,
                similarity_threshold=similarity_threshold,
            )
            logger.info(
                f"Functions for `{action_description}`: {[tool.unique_id for tool in tools]} "
            )
            tool_lookup[action_description] = tools
            actions_with_tools.append((action_description, tools))
        return actions_with_tools

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
        tools: list[Tool],
        messages: Optional[list] = None,
    ) -> str:
        tool_definitions = [tool.definition for tool in tools]
        if messages is None:
            messages = self.messages
        response = self._get_response(
            msgs=messages,
            tools=tool_definitions,
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
                tools=tool_definitions,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
        messages.append(response_message)
        return response_message.content

    @staticmethod
    def _run_ruff(code: str) -> str | None:
        file_path = "ruff_tmp.py"
        with open(file_path, "w") as file:
            file.write(code)
        try:
            result = subprocess.run(
                ["ruff", "check", "--fix", file_path],
                capture_output=True,
                text=True,
                check=True,
            )
            if result.returncode == 0:
                ruff_output = None
            else:
                ruff_output = result.stdout
        except subprocess.CalledProcessError as e:
            logging.error("Error running ruff:", e.stderr)
            ruff_output = "There was an error running ruff."
        if ruff_output is None:
            subprocess.run(["ruff", "format", file_path])
        os.remove(file_path)
        return ruff_output

    def _generate_code(self, task_description: str, max_retries: int = 3) -> str | None:
        _msgs = [
            {
                "role": "system",
                "content": TECH_LEAD,
            },
            {
                "role": "user",
                "content": task_description,
            },
        ]
        response = self._get_response(msgs=_msgs)
        code = response.choices[0].message.content
        code = code[9:-3] if code.startswith("```") else code
        retries = 0
        while True:
            if retries >= max_retries:
                logger.info(
                    f"Failed generating code for the task `{task_description}`. Aborting."
                )
                return None
            try:
                ast.parse(code)
            except SyntaxError:
                logger.info(f"Syntax check #{retries} failed.")
                retries += 1
                _msgs.append(
                    {
                        "role": "user",
                        "content": (
                            "The code was not executable. "
                            "Try again and write it in a way so that I can copy paste it."
                        ),
                    }
                )
                response = self._get_response(msgs=_msgs)
                code = response.choices[0].message.content
                code = code[9:-3] if code.startswith("```") else code
                continue
            break
        while True:
            if retries >= max_retries:
                logger.info(
                    f"Failed generating code for the task `{task_description}`. Aborting."
                )
                return None
            ruff_output = self._run_ruff(code)
            if ruff_output:
                logger.info(f"Format check #{retries} failed.")
                retries += 1
                _msgs.append(
                    {
                        "role": "user",
                        "content": (
                            "The code did not pass the style check. "
                            "Try again and write it in a way so that I can copy paste it."
                        ),
                    }
                )
                response = self._get_response(msgs=_msgs)
                code = response.choices[0].message.content
                code = code[9:-3] if code.startswith("```") else code
                continue
            break
        logger.info(f"Successfully generated code for the task `{task_description}`.")
        return code
