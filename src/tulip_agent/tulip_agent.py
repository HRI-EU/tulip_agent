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
TulipAgent variations; use a vector store as a tool library.
"""
import ast
import json
import logging
from abc import ABC
from typing import Optional

from .base_agent import LlmAgent
from .constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from .prompts import (
    AUTO_TULIP_PROMPT,
    RECURSIVE_TASK_DECOMPOSITION,
    SOLVE_WITH_TOOLS,
    TASK_DECOMPOSITION,
    TECH_LEAD,
    TOOL_CREATE,
    TOOL_PROMPT,
    TOOL_SEARCH,
    TOOL_UPDATE,
    TULIP_COT_PROMPT,
)
from .tool_library import ToolLibrary


logger = logging.getLogger(__name__)


class TulipAgent(LlmAgent, ABC):
    def __init__(
        self,
        instructions: str,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 3,
        search_similarity_threshold: float = None,
    ) -> None:
        super().__init__(
            instructions=instructions,
            model=model,
            temperature=temperature,
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

    def search_tools(self, action_descriptions: list[str]):
        json_res, hash_res = [], []
        for action_description in action_descriptions:
            res = self.tool_library.search(
                problem_description=action_description,
                top_k=self.top_k_functions,
                similarity_threshold=self.search_similarity_threshold,
            )["documents"]
            if res:
                json_res_ = [json.loads(e) for e in res[0] if e not in hash_res]
                hash_res.extend(res)
                logger.info(
                    f"Functions for `{action_description}`: {json.dumps(json_res_)}"
                )
                json_res.extend(json_res_)
        return json_res

    def execute_search_tool_call(
        self,
        tool_calls: list,
        track_history: bool,
    ) -> list:
        tools = []
        for tool_call in tool_calls:
            func = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            assert func == "search_tools", f"Unexpected tool call: {func}"

            # search tulip for function with args
            logger.info(f"Tool search for: {str(args)}")
            tools_ = self.search_tools(**args)
            logger.info(f"Tools found: {str(tools_)}")
            tools.extend(tools_)
            if track_history:
                self.messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func,
                        "content": "Successfully provided suitable tools.",
                    }
                )
        return tools

    def run_with_tools(self, tools: list[dict]) -> str:
        response = self._get_response(
            msgs=self.messages,
            tools=tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        while tool_calls:
            self.messages.append(response_message)

            for tool_call in tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                function_response, error = self.tool_library.execute(
                    function_id=func_name, function_args=func_args
                )
                if error:
                    func_name = "invalid_tool_call"
                    tool_call.function.name = func_name
                self.messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": str(function_response),
                    }
                )
                logger.info(
                    f"Function {func_name} returned `{str(function_response)}` for arguments {func_args}."
                )

            response = self._get_response(
                msgs=self.messages,
                tools=tools,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
        self.messages.append(response_message)
        logger.info(
            f"{self.__class__.__name__} returns response: {response_message.content}"
        )
        return response_message.content


class MinimalTulipAgent(TulipAgent):
    def __init__(
        self,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 10,
        instructions: Optional[str] = None,
    ) -> None:
        super().__init__(
            instructions=(
                TOOL_PROMPT + "\n\n" + instructions if instructions else TOOL_PROMPT
            ),
            model=model,
            temperature=temperature,
            tool_library=tool_library,
            top_k_functions=top_k_functions,
        )

    def query(
        self,
        prompt: str,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")

        # Search for tools directly with user prompt; do not track the search
        tools = self.search_tools(action_descriptions=[prompt])

        # Run with tools
        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        return self.run_with_tools(tools=tools)


class NaiveTulipAgent(TulipAgent):
    def __init__(
        self,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 3,
        instructions: Optional[str] = None,
    ) -> None:
        super().__init__(
            instructions=(
                TOOL_PROMPT + "\n\n" + instructions if instructions else TOOL_PROMPT
            ),
            model=model,
            temperature=temperature,
            tool_library=tool_library,
            top_k_functions=top_k_functions,
        )

    def query(
        self,
        prompt: str,
        tool_search_retries: int = 3,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")

        # Search for tools, but do not track the search
        _msgs = [
            {
                "role": "system",
                "content": self.instructions,
            },
            {
                "role": "user",
                "content": f"Search for appropriate tools for reacting to the following user request: {prompt}.",
            },
        ]
        tools, retries = None, 0
        while not tools:
            function_response = self._get_response(
                msgs=_msgs,
                tools=[self.search_tools_description],
                tool_choice={"type": "function", "function": {"name": "search_tools"}},
            )
            response_message = function_response.choices[0].message
            tool_calls = response_message.tool_calls

            # More than one tool call - several searches should be combined in one call
            if (lntc := len(tool_calls)) > 1:
                logger.info(
                    f"Tool search invalid: Returned {lntc} instead of 1 search call. Retrying."
                )
                _msgs.append(
                    {
                        "tool_call_id": tool_calls[0].id,
                        "role": "tool",
                        "name": "search_tools",
                        "content": "Error: Invalid number of tool calls; return a single call to `search_tools`.",
                    }
                )
            # Try running search for tools from tool call
            else:
                try:
                    tools = self.execute_search_tool_call(
                        tool_calls=tool_calls, track_history=False
                    )
                    break
                except Exception as e:
                    logger.info(
                        f"Invalid tool call for `search_tools`: `{e}`. Retrying."
                    )
                    _msgs.append(
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
        return self.run_with_tools(tools=tools)


class CotTulipAgent(TulipAgent):
    def __init__(
        self,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 3,
        search_similarity_threshold: float = 0.35,
        instructions: Optional[str] = None,
    ) -> None:
        super().__init__(
            instructions=(
                TULIP_COT_PROMPT + "\n\n" + instructions
                if instructions
                else TULIP_COT_PROMPT
            ),
            model=model,
            temperature=temperature,
            tool_library=tool_library,
            top_k_functions=top_k_functions,
            search_similarity_threshold=search_similarity_threshold,
        )

    def recursively_search_tool(
        self,
        tool_calls: list,
        depth: int,
        max_depth: int = 2,
    ) -> list:
        new_tools = []
        for tc in tool_calls:
            tools_ = self.execute_search_tool_call(tool_calls=[tc], track_history=True)
            if not tools_ and depth < max_depth:
                subtasks = self.decompose_task(
                    task=tc, base_prompt=RECURSIVE_TASK_DECOMPOSITION
                )
                tool_calls = self.get_search_tool_calls(tasks=subtasks)
                tools_ = self.recursively_search_tool(
                    tool_calls=tool_calls,
                    depth=depth + 1,
                    max_depth=max_depth,
                )
            for t in tools_:
                if t not in new_tools:
                    new_tools.append(t)
        return new_tools

    def decompose_task(
        self,
        task: str,
        base_prompt: str,
    ) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": base_prompt.format(prompt=task),
            }
        )
        actions_response = self._get_response(msgs=self.messages)
        actions_response_message = actions_response.choices[0].message
        self.messages.append(actions_response_message)
        logger.info(f"{actions_response_message=}")
        return actions_response_message.content

    def get_search_tool_calls(self, tasks: str):
        self.messages.append(
            {
                "role": "user",
                "content": TOOL_SEARCH.format(tasks=tasks),
            }
        )
        function_response = self._get_response(
            msgs=self.messages,
            tools=[self.search_tools_description],
            tool_choice={"type": "function", "function": {"name": "search_tools"}},
        )
        response_message = function_response.choices[0].message
        tool_calls = response_message.tool_calls
        self.messages.append(response_message)
        assert (
            lntc := len(tool_calls)
        ) == 1, f"Not exactly one tool search executed, but {lntc}."
        return tool_calls

    def query(
        self,
        prompt: str,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")

        # Get tasks from user input and initiate recursive tool search
        tasks = self.decompose_task(task=prompt, base_prompt=TASK_DECOMPOSITION)
        tool_calls = self.get_search_tool_calls(tasks)
        tools = self.recursively_search_tool(tool_calls=tool_calls, depth=0)

        # Run with tools
        self.messages.append(
            {
                "role": "user",
                "content": SOLVE_WITH_TOOLS.format(steps=tasks),
            }
        )
        return self.run_with_tools(tools=tools)


class AutoTulipAgent(TulipAgent):
    def __init__(
        self,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 1,
        instructions: Optional[str] = None,
    ) -> None:
        super().__init__(
            instructions=(
                AUTO_TULIP_PROMPT + "\n\n" + instructions
                if instructions
                else AUTO_TULIP_PROMPT
            ),
            model=model,
            temperature=temperature,
            tool_library=tool_library,
            top_k_functions=top_k_functions,
        )
        self.create_tool_description = {
            "type": "function",
            "function": {
                "name": "create_tool",
                "description": "Generate a tool and add it to your tool library.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string",
                            "description": "A textual description of the task to be solved with a Python function.",
                        },
                    },
                    "required": ["task_descriptions"],
                },
            },
        }
        self.update_tool_description = {
            "type": "function",
            "function": {
                "name": "update_tool",
                "description": "Update a tool in your tool library.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tool_name": {
                            "type": "string",
                            "description": "The tool's unique name, as returned by the tool search.",
                        },
                        "instruction": {
                            "type": "string",
                            "description": "A textual description of the changes to be made to the tool.",
                        },
                    },
                    "required": ["tool_name", "instruction"],
                },
            },
        }
        self.delete_tool_description = {
            "type": "function",
            "function": {
                "name": "delete_tool",
                "description": (
                    "Delete a tool from your tool library. "
                    "You may have to look up the exact name using the search_tools tool."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tool_name": {
                            "type": "string",
                            "description": "The tool's unique name, as returned by the tool search.",
                        },
                    },
                    "required": ["tool_name"],
                },
            },
        }
        self.decompose_task_description = {
            "type": "function",
            "function": {
                "name": "decompose_task",
                "description": "Decompose a task into its subtasks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "A description of the task that should be decomposed into steps.",
                        },
                    },
                    "required": ["task"],
                },
            },
        }
        self.tools = [
            self.search_tools_description,
            self.create_tool_description,
            self.update_tool_description,
            self.delete_tool_description,
            self.decompose_task_description,
        ]

    def _generate_code(
        self, task_description: str, gen_attempts: int = 0
    ) -> str | None:
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
        while True:
            if gen_attempts > 3:
                logger.info(
                    f"Failed generating code for the task `{task_description}`. Aborting."
                )
                return None
            try:
                ast.parse(code)
            except SyntaxError:
                logger.info(f"Attempt {gen_attempts} failed.")
                gen_attempts += 1
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
                continue
            break
        logger.info(f"Successfully generated code for the task `{task_description}`.")
        return code

    def create_tool(self, task_description: str) -> str:
        # gen code
        task_description_ = TOOL_CREATE.format(task_description=task_description)
        code = self._generate_code(task_description=task_description_)
        if code is None:
            failure_msg = (
                f"Failed generating a function for the task `{task_description}`."
            )
            logger.info(failure_msg)
            return failure_msg
        # write to file
        function_name = code.split("def ")[1].split("(")[0]
        module_name = f"{function_name}_module"
        with open(f"{module_name}.py", "w") as f:
            f.write(code)
        # add module to tool library
        self.tool_library.load_functions_from_file(
            module_name=module_name, function_names=[f"{function_name}"]
        )
        success_msg = f"Made function `{module_name}__{function_name}` available via the tool library."
        logger.info(success_msg)
        return success_msg

    def update_tool(self, tool_name: str, instruction: str) -> str:
        # NOTE: updating is currently only supported for modules with single functions
        # retrieve old code
        module_path = self.tool_library.function_origins[tool_name]["module_path"]
        with open(module_path, "r") as m:
            old_code = m.read()
        # generate replacement
        task_description = TOOL_UPDATE.format(code=old_code, instruction=instruction)
        code = self._generate_code(task_description=task_description)
        if code is None:
            failure_msg = f"Failed updating the code for {tool_name}."
            logger.info(failure_msg)
            return failure_msg
        # reload tool library
        with open(module_path, "w") as m:
            m.write(code)
        self.tool_library.update_function(function_id=tool_name)
        success_msg = f"Successfully updated `{tool_name}`."
        logger.info(success_msg)
        return success_msg

    def delete_tool(self, tool_name: str) -> str:
        self.tool_library.remove_function(function_id=tool_name)
        return f"Removed tool {tool_name} from the tool library."

    def decompose_task(self, task: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are an expert in planning and task decomposition.",
            },
            {
                "role": "user",
                "content": TASK_DECOMPOSITION.format(prompt=task),
            },
        ]
        decomposition_response = self._get_response(msgs=messages)
        decomposed_tasks = decomposition_response.choices[0].message
        logger.info(f"{decomposed_tasks=}")
        return decomposed_tasks.content

    def query(
        self,
        prompt: str,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")
        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self._get_response(
            msgs=self.messages,
            tools=self.tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        while tool_calls:
            self.messages.append(response_message)

            for tool_call in tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                cud_lookup = {
                    "create_tool": {
                        "log_message": f"Creating tool: {str(func_args)}",
                        "function": self.create_tool,
                    },
                    "update_tool": {
                        "log_message": f"Updating tool: {str(func_args)}",
                        "function": self.update_tool,
                    },
                    "delete_tool": {
                        "log_message": f"Deleting tool: {str(func_args)}",
                        "function": self.delete_tool,
                    },
                }

                if func_name == "decompose_task":
                    logger.info(f"Task decomposition for: {func_args['task']}")
                    subtasks = self.decompose_task(**func_args)
                    logger.info(f"Subtasks: {str(subtasks)}")
                    self.messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": f"Subtasks for `{func_args['task']}` are: {subtasks}",
                        }
                    )
                elif func_name == "search_tools":
                    logger.info(f"Tool search for: {str(func_args)}")
                    tools_ = self.search_tools(**func_args)
                    logger.info(f"Tools found: {str(tools_)}")
                    self.tools.extend(tools_)
                    tool_names_ = [td["function"]["name"] for td in tools_]
                    if tool_names_:
                        status = f"Successfully provided suitable tools: {tool_names_}."
                    else:
                        status = "Could not find suitable tools."
                    self.messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": status,
                        }
                    )
                elif func_name in cud_lookup.keys():
                    logger.info(cud_lookup[func_name]["log_message"])
                    status = cud_lookup[func_name]["function"](**func_args)
                    self.messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": f"{status}",
                        }
                    )
                else:
                    function_response = self.tool_library.execute(
                        function_id=func_name, function_args=func_args
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
                        f"Function {func_name} returned `{str(function_response)}` for arguments {func_args}."
                    )

            response = self._get_response(
                msgs=self.messages,
                tools=self.tools,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
        self.messages.append(response_message)
        logger.info(
            f"{self.__class__.__name__} returns response: {response_message.content}"
        )
        return response_message.content
