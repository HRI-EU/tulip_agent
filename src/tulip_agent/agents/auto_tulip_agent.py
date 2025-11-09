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
AutoTulipAgent variant; uses a vector store as a tool library, has CRUD access to the library.
"""
import json
import logging
from typing import Optional

from openai import AzureOpenAI, OpenAI

from tulip_agent.agents.prompts import (
    AUTO_TULIP_PROMPT,
    TASK_DECOMPOSITION,
    TOOL_CREATE,
    TOOL_UPDATE,
)
from tulip_agent.agents.tulip_agent import TulipAgent
from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from tulip_agent.tool import InternalTool, Tool
from tulip_agent.tool_library import ToolLibrary


logger = logging.getLogger(__name__)


class AutoTulipAgent(TulipAgent):
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
        search_similarity_threshold: float | None = None,
    ) -> None:
        if base_model is None and reasoning_model is None:
            base_model = BASE_LANGUAGE_MODEL
            temperature = BASE_TEMPERATURE
        super().__init__(
            instructions=(instructions or AUTO_TULIP_PROMPT),
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

        for func in (
            self.create_tool,
            self.update_tool,
            self.delete_tool,
            self.decompose_task,
            self.search_tools,
        ):
            tool_ = InternalTool(
                function_name=func.__name__,
                definition=self.tool_library.function_analyzer.analyze_function(func),
                function=func,
            )
            self.default_tools.append(tool_)
            self.tool_library.tools[tool_.unique_id] = tool_
        self.tools = self.default_tools.copy()

    def create_tool(self, task_description: str) -> str:
        """
        Generate a tool and add it to your tool library.

        :param task_description: A textual description of the task to be solved with a Python function.
        :return: Success information for the tool creation.
        """
        logger.info(f"Creating tool: {task_description}")
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
        new_tool = self.tool_library.load_functions_from_file(
            module_name=module_name, function_names=[f"{function_name}"]
        )[0]
        self.tools.append(new_tool)
        success_msg = (
            f"Made tool `{new_tool.unique_id}` available via the tool library."
        )
        logger.info(success_msg)
        return success_msg

    def update_tool(self, tool_name: str, instruction: str) -> str:
        """
        Update a tool in your tool library.

        :param tool_name: The tool's unique name, as returned by the tool search.
        :param instruction: A textual description of the changes to be made to the tool.
        :return: Success information for the tool update.
        """
        # NOTE: updating is currently only supported for modules with single functions
        logger.info(f"Updating tool {tool_name}: {instruction}")
        if tool_name in [dt.unique_id for dt in self.default_tools]:
            return f"Unable to update {tool_name} because it is a default tool."

        # retrieve old code
        module_path = self.tool_library.tools[tool_name].module_path
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
        updated_tool = self.tool_library.update_tool(tool_id=tool_name)
        self.tools = [t for t in self.tools if t.unique_id != tool_name]
        self.tools.append(updated_tool)
        success_msg = f"Successfully updated `{tool_name}`."
        logger.info(success_msg)
        return success_msg

    def delete_tool(self, tool_name: str) -> str:
        """
        Delete a tool from your tool library.
        You may have to look up the exact name using the search_tools tool.

        :param tool_name: The tool's unique name, as returned by the tool search.
        :return: Success information for the tool deletion.
        """
        logger.info(f"Deleting tool: {tool_name}")
        if tool_name in [dt.unique_id for dt in self.default_tools]:
            return f"Unable to delete {tool_name} because it is a default tool."

        self.tool_library.remove_tool(tool_id=tool_name)
        self.tools = [t for t in self.tools if t.unique_id != tool_name]
        return f"Removed tool {tool_name} from the tool library."

    def decompose_task(self, task: str) -> str:
        """
        Decompose a task into its subtasks.

        :param task: A description of the task that should be decomposed into steps.
        :return: The subtasks into which the task was decomposed.
        """
        logger.info(f"Task decomposition for: {task}")
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
        decomposition_response = self._get_response(
            msgs=messages, response_format="json", reasoning=True
        )
        decomposed_tasks = decomposition_response.choices[0].message
        logger.info(f"{decomposed_tasks=}")
        res = json.loads(decomposed_tasks.content)
        subtasks = res["subtasks"]
        return f"Subtasks for `{task}` are: {subtasks}"

    def query(
        self,
        prompt: str,
    ) -> str:
        self.response = None
        logger.info(f"{self.__class__.__name__} received query: {prompt}")
        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self._get_response(
            msgs=self.messages,
            tools=[t.definition for t in self.tools],
            tool_choice="required",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        while not self.response:
            self.messages.append(response_message)

            if self.api_interaction_counter >= self.api_interaction_limit:
                error_message = f"Error: Reached API interaction limit of {self.api_interaction_limit}."
                logger.error(
                    f"{self.__class__.__name__} returns response: {error_message}"
                )
                return error_message

            for tool_call in tool_calls:
                func_name = tool_call.function.name
                try:
                    func_args = json.loads(tool_call.function.arguments)
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
                    self.messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": function_response,
                        }
                    )
                    continue

                if func_name == "search_tools":
                    logger.info(f"Tool search for: {str(func_args)}")
                    new_tools = [
                        tool
                        for partial in self.search_tools(
                            **func_args,
                            similarity_threshold=self.search_similarity_threshold,
                        )
                        for tool in partial[1]
                        if tool not in self.tools
                    ]
                    logger.info(f"Tools found: {str(new_tools)}")
                    self.tools.extend(new_tools)
                    tool_names_ = [new_tool.unique_id for new_tool in new_tools]
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
                else:
                    function_response, error = self.tool_library.execute(
                        tool_id=func_name, arguments=func_args
                    )
                    if error:
                        func_name = "invalid_tool_call"
                        tool_call.function.name = func_name
                        tool_call.function.arguments = "{}"
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
                tools=[t.definition for t in self.tools],
                tool_choice="required",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
        logger.info(f"{self.__class__.__name__} returns response: {self.response}")
        self.api_interaction_counter = 0
        return self.response
