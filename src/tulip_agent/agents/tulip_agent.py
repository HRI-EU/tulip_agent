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
TulipAgent ABC; uses a vector store as a tool library.
"""
import ast
import json
import logging
import os
import subprocess
import sys
import tempfile
from abc import ABC
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from openai import AzureOpenAI, OpenAI
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)

from tulip_agent.agents.base_agent import LlmAgent
from tulip_agent.agents.prompts import TECH_LEAD
from tulip_agent.tool import InternalTool, Tool
from tulip_agent.tool_execution import Job, execute_tool_calls
from tulip_agent.tool_library import ToolLibrary


logger = logging.getLogger(__name__)


class TulipAgent(LlmAgent, ABC):
    def __init__(
        self,
        instructions: str,
        tool_library: ToolLibrary,
        base_model: str | None,
        base_client: AzureOpenAI | OpenAI | None,
        reasoning_model: str | None,
        reasoning_client: AzureOpenAI | OpenAI | None,
        temperature: float | None,
        api_interaction_limit: int = 100,
        default_tools: Optional[list[Tool]] = None,
        top_k_functions: int = 3,
        search_similarity_threshold: float | None = None,
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
        self.tool_library = tool_library
        self.top_k_functions = top_k_functions
        self.search_similarity_threshold = search_similarity_threshold
        self.response: str | None = None

        if default_tools and not tool_library:
            raise ValueError("A tool library is required to set default tools.")
        if default_tools and (
            missing_tools := [
                tool.unique_id
                for tool in default_tools
                if tool.unique_id not in tool_library.tools
            ]
        ):
            raise ValueError(
                f"Tools {', '.join(missing_tools)} not available in tool library."
            )
        stop_tool = InternalTool(
            function_name=self.stop.__name__,
            definition=self.tool_library.function_analyzer.analyze_function(self.stop),
            function=self.stop,
        )
        self.default_tools = (
            default_tools + [stop_tool] if default_tools else [stop_tool]
        )
        self.tool_library.tools[stop_tool.unique_id] = stop_tool

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
                                "A list of strings with textual descriptions for the actions you want to execute. "
                                "The description should be generic enough to find generic and reusable tools."
                            ),
                        },
                    },
                    "required": ["action_descriptions"],
                },
            },
        }

    def stop(self, message: str) -> str:
        """
        Stop and return a final message to the user.

        :param message: The message to return.
        :return: The final response to be given to the user.
        """
        self.response = message
        return "Done."

    def search_tools(
        self,
        action_descriptions: list[str],
        similarity_threshold: Optional[float] = None,
    ) -> list[tuple[str, list[Tool]]]:
        """
        Search for tools in your tool library.

        :param action_descriptions: A list of strings with textual descriptions for the actions you want to execute.
            The description should be generic enough to find generic and reusable tools.
        :param similarity_threshold: Similarity threshold to use for searching.
        :return: A list of tuples with action descriptions and respective tools.
        """
        unique_actions = set(action_descriptions)
        tool_lookup = {}

        with ThreadPoolExecutor() as executor:
            future_to_action = {
                action: executor.submit(
                    self.tool_library.search,
                    problem_description=action,
                    top_k=self.top_k_functions,
                    similarity_threshold=similarity_threshold,
                )
                for action in unique_actions
            }
            for action, future in future_to_action.items():
                tools = future.result()
                if self.default_tools:
                    tools.extend(
                        [tool for tool in self.default_tools if tool not in tools]
                    )
                logger.info(
                    f"Functions for `{action}`: {[tool.unique_id for tool in tools]}"
                )
                tool_lookup[action] = tools

        return [(action, tool_lookup[action]) for action in action_descriptions]

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
        self.response = None
        tool_definitions = [tool.definition for tool in tools]
        if messages is None:
            messages = self.messages
        response = self._get_response(
            msgs=messages,
            tools=tool_definitions,
            tool_choice="required",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        while not self.response:
            messages.append(response_message)

            if self.api_interaction_counter >= self.api_interaction_limit:
                error_message = f"Error: Reached API interaction limit of {self.api_interaction_limit}."
                logger.warning(f"{self.__class__.__name__}: {error_message}")
                return error_message

            self._execute_tool_calls(tool_calls=tool_calls, messages=messages)

            response = self._get_response(
                msgs=messages,
                tools=tool_definitions,
                tool_choice="required",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
        return self.response

    def _execute_tool_calls(self, tool_calls: list, messages: list) -> None:
        if not tool_calls:
            return

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
                function_response = (
                    f"Error: Invalid arguments for {func_name} "
                    f"(previously {generated_func_name}): {e}"
                )
                tool_messages[i] = {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": func_name,
                    "content": function_response,
                }
                continue

            if func_name not in self.tool_library.tools:
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
                    tool=self.tool_library.tools[func_name],
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
            messages.append(tool_message)
            logger.info(
                (
                    f"Function {tool_message['name']} returned `{tool_message['content']}` "
                    f"for arguments {tool_call.function.arguments}."
                )
            )

    @staticmethod
    def _run_ruff(code: str) -> str | None:
        fd, file_path = tempfile.mkstemp(suffix=".py", prefix="ruff_tmp_")
        os.close(fd)
        with open(file_path, "w") as file:
            file.write(code)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "ruff", "check", "--fix", file_path],
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
            subprocess.run(
                [sys.executable, "-m", "ruff", "format", file_path], check=True
            )
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
