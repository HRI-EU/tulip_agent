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
CotTulipAgent variant; uses a vector store as a tool library and COT for task decomposition.
"""
import json
import logging
from typing import Optional

from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)

from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from tulip_agent.prompts import (
    RECURSIVE_TASK_DECOMPOSITION,
    SOLVE_WITH_TOOLS,
    TOOL_SEARCH,
    TULIP_COT_PROMPT,
)
from tulip_agent.tool_library import ToolLibrary

from .llm_agent import ModelServeMode
from .tulip_agent import TulipAgent


logger = logging.getLogger(__name__)


class CotTulipAgent(TulipAgent):
    def __init__(
        self,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        model_serve_mode: ModelServeMode = ModelServeMode.OPENAI,
        api_interaction_limit: int = 100,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 3,
        search_similarity_threshold: float = None,
        instructions: Optional[str] = None,
        decomposition_prompt: str = RECURSIVE_TASK_DECOMPOSITION,
    ) -> None:
        super().__init__(
            instructions=(instructions or TULIP_COT_PROMPT),
            model=model,
            temperature=temperature,
            model_serve_mode=model_serve_mode,
            api_interaction_limit=api_interaction_limit,
            tool_library=tool_library,
            top_k_functions=top_k_functions,
            search_similarity_threshold=search_similarity_threshold,
        )
        self.decomposition_prompt = decomposition_prompt

    def recursively_search_tool(
        self,
        tool_call: ChatCompletionMessageToolCall,
        depth: int,
        max_depth: int = 2,
    ) -> tuple[list, list]:
        new_tools, new_tasks = [], []
        tools_by_tasks = self.execute_search_tool_call(
            tool_call=tool_call, track_history=True
        )
        for task, tools in tools_by_tasks:
            if not tools and depth < max_depth:
                subtasks = self.decompose_task(
                    task=task,
                    base_prompt=self.decomposition_prompt,
                )
                subtask_str = ""
                for c, subtask in enumerate(subtasks):
                    subtask_str += f"{str(c+1)}. {subtask}"
                tool_call = self.get_search_tool_call(tasks=subtask_str)
                tools_, tasks_ = self.recursively_search_tool(
                    tool_call=tool_call,
                    depth=depth + 1,
                    max_depth=max_depth,
                )
                for t in tools_:
                    if t not in new_tools:
                        new_tools.append(t)
                new_tasks.append(tasks_)
            else:
                for t in tools:
                    if t not in new_tools:
                        new_tools.append(t)
                new_tasks.append(task)
        return new_tools, new_tasks

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
        actions_response = self._get_response(
            msgs=self.messages, response_format="json"
        )
        actions_response_message = actions_response.choices[0].message
        self.messages.append(actions_response_message)
        logger.info(f"{actions_response_message=}")
        res = json.loads(actions_response_message.content)
        return res["subtasks"]

    def get_search_tool_call(self, tasks: str):
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
        return tool_calls[0]

    def query(
        self,
        prompt: str,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")

        # Get tasks from user input and initiate recursive tool search
        tasks = self.decompose_task(task=prompt, base_prompt=self.decomposition_prompt)
        tool_call = self.get_search_tool_call(tasks)
        tools, general_tasks = self.recursively_search_tool(
            tool_call=tool_call, depth=0
        )

        # Run with tools
        task_str = ""
        for c, task in enumerate(tasks):
            task_str += f"{str(c+1)}. {task}\n"
        logger.info(f"{task_str=}")
        self.messages.append(
            {
                "role": "user",
                "content": SOLVE_WITH_TOOLS.format(steps=task_str),
            }
        )
        response = self.run_with_tools(tools=tools)
        logger.info(f"{self.__class__.__name__} returns response: {response}")
        return response
