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
DfsTulipAgent variant; uses a vector store as a tool library and does DFS style planning.
"""
import copy
import json
import logging
from typing import Optional

from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from tulip_agent.prompts import (
    TOOL_CREATE,
    TREE_TULIP_AGGREGATE_PROMPT,
    TREE_TULIP_DECOMPOSITION_PROMPT,
    TREE_TULIP_PARAPHRASE_PROMPT,
    TREE_TULIP_REPLAN_PROMPT,
    TREE_TULIP_SYSTEM_PROMPT,
    TREE_TULIP_TASK_PROMPT,
)
from tulip_agent.task import Task
from tulip_agent.tool import Tool
from tulip_agent.tool_library import ToolLibrary

from .llm_agent import ModelServeMode
from .tulip_agent import TulipAgent


logger = logging.getLogger(__name__)


class DfsTulipAgent(TulipAgent):
    def __init__(
        self,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        model_serve_mode: ModelServeMode = ModelServeMode.OPENAI,
        api_interaction_limit: int = 100,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 5,
        search_similarity_threshold: float = 1.25,
        max_recursion_depth: int = 3,
        max_paraphrases: int = 1,
        max_replans: int = 1,
        instructions: Optional[str] = None,
        plot_task_tree: bool = False,
    ) -> None:
        super().__init__(
            instructions=(
                TREE_TULIP_SYSTEM_PROMPT + "\n\n" + instructions
                if instructions
                else TREE_TULIP_SYSTEM_PROMPT
            ),
            model=model,
            temperature=temperature,
            model_serve_mode=model_serve_mode,
            api_interaction_limit=api_interaction_limit,
            tool_library=tool_library,
            top_k_functions=top_k_functions,
            search_similarity_threshold=search_similarity_threshold,
        )
        self.max_recursion_depth = max_recursion_depth
        self.max_paraphrases = max_paraphrases
        self.max_replans = max_replans
        self.plot_task_tree = plot_task_tree
        self.task = None

    def query(
        self,
        prompt: str,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")
        initial_task = Task(description=prompt)
        self.task = self.recurse(task=initial_task, recursion_level=0)
        logger.debug(self.task.__dict__)
        if self.plot_task_tree:
            self.task.plot()
        logger.info(f"{self.__class__.__name__} returns response: {self.task.result}")
        return self.task.result

    def decompose_task(
        self,
        task: Task,
        tool_names: list[str],
        base_prompt: str,
    ) -> str:
        previous_info = (
            "\n".join(
                [
                    f"{c + 1}. {p.description}: {p.result}"
                    for c, p in enumerate(task.get_predecessors()[::-1])
                ]
            )
            if task.get_predecessors()
            else "[]"
        )
        messages = [
            {
                "role": "user",
                "content": base_prompt.format(
                    task=task.description, tools=tool_names, previous=previous_info
                ),
            },
        ]
        logger.debug(f"Decomposition prompt: {messages[-1]['content']}")
        response = self._get_response(msgs=messages, response_format="json")
        decompose_response_message = response.choices[0].message
        logger.info(f"{decompose_response_message=}")
        res = json.loads(decompose_response_message.content)
        return res["subtasks"]

    def create_tool(self, task_description: str) -> None | Tool:
        # generate code
        task_description_ = TOOL_CREATE.format(task_description=task_description)
        code = self._generate_code(task_description=task_description_)
        if code is None:
            return None
        # write to file
        function_name = code.split("def ")[1].split("(")[0]
        module_name = f"{function_name}_module"
        with open(f"{module_name}.py", "w") as f:
            f.write(code)
        # add module to tool library
        new_tool = self.tool_library.load_functions_from_file(
            module_name=module_name, function_names=[f"{function_name}"]
        )[0]
        logger.info(
            f"Made tool `{module_name}__{function_name}` available via the tool library."
        )
        return new_tool

    def recurse(
        self,
        task: Task,
        recursion_level: int,
    ) -> Task:
        logger.debug(f"Recursing for task: {task}")

        if recursion_level > self.max_recursion_depth:
            task.result = f"Error: Aborting decomposition beyond the level of `{task.description}`"
            return task

        _, generic_tools = self.search_tools(action_descriptions=[task.description])[0]
        _, tools = self.search_tools(
            action_descriptions=[task.description],
            similarity_threshold=self.search_similarity_threshold,
        )[0]

        # decompose if sensible
        if task.generated_tools:
            subtask_descriptions = []
        elif len(task.subtasks) == 0:
            subtask_descriptions = self.decompose_task(
                task=task,
                tool_names=[gt.unique_id for gt in generic_tools],
                base_prompt=TREE_TULIP_DECOMPOSITION_PROMPT,
            )
        else:
            # TODO: add failure info
            failed = "\n".join(
                [
                    ", ".join([st.description for st in subtask_list])
                    for subtask_list in task.subtasks
                ]
            )
            subtask_descriptions = self.decompose_task(
                task=task,
                tool_names=[gt.unique_id for gt in generic_tools],
                base_prompt=TREE_TULIP_REPLAN_PROMPT.replace("{failed}", failed),
            )
        if len(subtask_descriptions) == 1:
            subtask_descriptions = []
        logger.debug(f"{subtask_descriptions=}")

        if subtask_descriptions:
            subtasks = [
                Task(description=d, supertask=task) for d in subtask_descriptions
            ]
            for s1, s2 in zip(subtasks, subtasks[1:]):
                s1.successor = s2
                s2.predecessor = s1
            task.subtasks.append(
                [self.recurse(subtask, recursion_level + 1) for subtask in subtasks]
            )
            # backtrack
            if any([st.result.startswith("Error: ") for st in task.subtasks[-1]]):
                if len(task.subtasks) > self.max_replans:
                    sequences = "\n".join(
                        [
                            " - ".join([st.description for st in subtask_list])
                            for subtask_list in task.subtasks
                        ]
                    )
                    # TODO: add failure info
                    task.result = f"Error: Reached maximum replans. Invalid subplans tried are:\n{sequences}"
                    return task
                else:
                    return self.recurse(task=task, recursion_level=recursion_level)
            # aggregate subtask results
            subtask_information = "\n".join(
                f"{c+1}. {st.description}: {st.result}"
                for c, st in enumerate(task.subtasks[-1])
            )
            messages = [
                {
                    "role": "user",
                    "content": TREE_TULIP_AGGREGATE_PROMPT.format(
                        task=task.description,
                        information=subtask_information,
                    ),
                },
            ]
            response = self._get_response(msgs=messages).choices[0].message.content
            task.result = (
                response
                if response != '""'
                else "Error: Could not solve the task based on its subtasks' results."
            )
        else:
            # execute with tools
            task.tool_candidates = tools
            logger.debug(f"Executing with tools: {task.description} - {tools}")
            if tools:
                previous_info = "\n".join(
                    [
                        f"{c+1}. {p.description}: {p.result}"
                        for c, p in enumerate(task.get_predecessors()[::-1])
                    ]
                )
                messages = [
                    {
                        "role": "user",
                        "content": TREE_TULIP_TASK_PROMPT.format(
                            task=task.description, previous=previous_info
                        ),
                    },
                ]
                logger.debug(f"Execution prompt: {messages[-1]['content']}")
                response = self.run_with_tools(tools=tools, messages=messages)
                task.result = (
                    response
                    if response != '""'
                    else f"Error: Could not solve the task `{task.description}` with the tools {tools}."
                )
            else:
                # paraphrase
                if len(task.paraphrased_variants) < self.max_paraphrases:
                    messages = [
                        {
                            "role": "user",
                            "content": TREE_TULIP_PARAPHRASE_PROMPT.format(
                                task=task.description,
                            ),
                        },
                    ]
                    # TODO: also include other prior wordings, retrieve from list of paraphrased_variants
                    paraphrased_description = (
                        self._get_response(msgs=messages).choices[0].message.content
                    )
                    task.paraphrased_variants.append(copy.copy(task))
                    task.description = paraphrased_description
                    return self.recurse(task=task, recursion_level=recursion_level)
                elif len(task.generated_tools) == 0:
                    # create new tool
                    new_tool = self.create_tool(task_description=task.description)
                    if new_tool:
                        task.generated_tools.append(new_tool)
                        return self.recurse(task=task, recursion_level=recursion_level)
                    else:
                        task.result = (
                            "Error: Could not generate code for a suitable tool."
                        )
        return task
