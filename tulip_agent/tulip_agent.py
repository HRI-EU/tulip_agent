#!/usr/bin/env python3
"""
TulipAgent variations; use a vector store for narrowing down tool search.
"""
import ast
import json
import logging

from abc import ABC, abstractmethod

from openai import OpenAI, OpenAIError

from .constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from .prompts import (
    AUTO_TULIP_PROMPT,
    RECURSIVE_TASK_DECOMPOSITION,
    SOLVE_WITH_TOOLS,
    TASK_DECOMPOSITION,
    TECH_LEAD,
    TOOL_PROMPT,
    TOOL_SEARCH,
    TULIP_COT_PROMPT,
)
from .tool_library import ToolLibrary


logger = logging.getLogger(__name__)


class TulipBaseAgent(ABC):
    def __init__(
        self,
        instructions: str,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 3,
        search_similarity_threshold: float = None,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.instructions = instructions
        self.tool_library = tool_library
        self.top_k_functions = top_k_functions
        self.openai_client = OpenAI()
        self.search_similarity_threshold = search_similarity_threshold

        self.messages = []
        if self.instructions:
            self.messages.append({"role": "system", "content": self.instructions})

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
                            "description": "A list of textual description for the actions you want to execute.",
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

    def _get_response(
        self,
        msgs: list[dict[str, str]],
        model: str = None,
        temperature: float = None,
        tools: list = None,
        tool_choice: str = "auto",
    ):
        response = None
        while not response:
            params = {
                "model": model if model else self.model,
                "messages": msgs,
                "temperature": temperature if temperature else self.temperature,
            }
            if tools:
                params["tools"] = tools
                params["tool_choice"] = tool_choice
            try:
                response = self.openai_client.chat.completions.create(**params)
            except OpenAIError as e:
                logger.error(e)
        logger.info(
            f"Usage for {response.id} in tokens: "
            f"{response.usage.prompt_tokens} prompt and {response.usage.completion_tokens} completion."
        )
        return response

    @abstractmethod
    def query(
        self,
        prompt: str,
    ) -> str:
        """
        Query the tulip agent, which has to figure out which tools to use.
        Includes two core steps: Identifying relevant tools and generating a response with these tools.

        :param prompt: User prompt
        :return: User-oriented final response
        """
        pass

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


class MinimalTulipAgent(TulipBaseAgent):
    def __init__(
        self,
        instructions: str = TOOL_PROMPT,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 10,
    ) -> None:
        super().__init__(
            instructions=instructions,
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


class NaiveTulipAgent(TulipBaseAgent):
    def __init__(
        self,
        instructions: str = TOOL_PROMPT,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 3,
    ) -> None:
        super().__init__(
            instructions=instructions,
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
        function_response = self._get_response(
            msgs=_msgs,
            tools=[self.search_tools_description],
            tool_choice={"type": "function", "function": {"name": "search_tools"}},
        )
        response_message = function_response.choices[0].message
        tool_calls = response_message.tool_calls
        assert (
            lntc := len(tool_calls)
        ) == 1, f"Not exactly one tool search executed, but {lntc}."

        tools = self.execute_search_tool_call(
            tool_calls=tool_calls, track_history=False
        )

        # Run with tools
        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        return self.run_with_tools(tools=tools)


class TulipCotAgent(TulipBaseAgent):
    def __init__(
        self,
        instructions: str = TULIP_COT_PROMPT,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 3,
        search_similarity_threshold: float = 0.35,
    ) -> None:
        super().__init__(
            instructions=instructions,
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
    ) -> tuple[list, list]:
        new_tools = []
        new_descriptions = []
        for tc in tool_calls:
            tools_ = self.execute_search_tool_call(tool_calls=[tc], track_history=True)
            if tools_:
                new_descriptions_ = [tc]
            elif depth >= max_depth:
                new_descriptions_ = [tc]
            else:
                subtasks = self.decompose_task(
                    task=tc, base_prompt=RECURSIVE_TASK_DECOMPOSITION
                )
                tool_calls = self.get_search_tool_calls(tasks=subtasks)
                tools_, new_descriptions_ = self.recursively_search_tool(
                    tool_calls=tool_calls,
                    depth=depth + 1,
                    max_depth=max_depth,
                )
            for t in tools_:
                if t not in new_tools:
                    new_tools.append(t)
            new_descriptions.extend(new_descriptions_)
        return new_tools, new_descriptions

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
        tools_, tasklist_ = self.recursively_search_tool(tool_calls=tool_calls, depth=0)
        tools = tools_
        tasklist = ""
        for c, t in enumerate(tasklist_):
            tasklist += f"{c}. {t}"
        logger.info(f"Complete tasklist: {tasklist}")

        # Run with tools
        self.messages.append(
            {
                "role": "user",
                "content": SOLVE_WITH_TOOLS.format(steps=tasks),
            }
        )
        return self.run_with_tools(tools=tools)


class AutoTulipAgent(TulipBaseAgent):
    def __init__(
        self,
        instructions: str = AUTO_TULIP_PROMPT,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 1,
    ) -> None:
        super().__init__(
            instructions=instructions,
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
                            "description": "The tools unique name, as returned by the tool search.",
                        },
                    },
                    "required": ["tool_name"],
                },
            },
        }
        self.tools = [
            self.search_tools_description,
            self.create_tool_description,
            self.delete_tool_description,
        ]

    def create_tool(self, task_description: str) -> str:
        # generate code
        _msgs = [
            {
                "role": "system",
                "content": TECH_LEAD,
            },
            {
                "role": "user",
                "content": f"Generate a Python function for the following task `{task_description}`.",
            },
        ]
        response = self._get_response(msgs=_msgs)
        code = response.choices[0].message.content
        gen_attempts = 0
        failure_message = (
            f"Failed generating a function for the task `{task_description}`. Aborting."
        )
        while True:
            if gen_attempts > 3:
                logger.info(failure_message)
                return failure_message
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
        # write code to file
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

    def delete_tool(self, tool_name: str) -> str:
        self.tool_library.remove_function(function_id=tool_name)
        return f"Removed tool {tool_name} from the tool library."

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

                if func_name == "search_tools":
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
                elif func_name == "create_tool":
                    logger.info(f"Creating tool for: {str(func_args)}")
                    status = self.create_tool(**func_args)
                    self.messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": f"{status}",
                        }
                    )
                elif func_name == "delete_tool":
                    logger.info(f"Deleting tool: {str(func_args)}")
                    status = self.delete_tool(**func_args)
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
