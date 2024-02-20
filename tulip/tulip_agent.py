#!/usr/bin/env python3
"""
The TulipAgent core
Process:
1) Initialize agent with a vector store
2) Take user request
3) Check for suitable functions, note that this is not tracked in message history
4) Run prompt with suitable tools
5) If applicable, run tool calls
6) Return response
"""
import json
import logging

from openai import OpenAI, OpenAIError

from prompts import BASE_PROMPT
from tool_library import ToolLibrary


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class TulipAgent:
    def __init__(
        self,
        model: str = "gpt-4-0125-preview",
        temperature: float = 0.0,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 1,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.instructions = BASE_PROMPT
        self.tool_library = tool_library
        self.top_k_functions = top_k_functions
        self.openai_client = OpenAI()

        self.messages = []
        if self.instructions:
            self.messages.append({"role": "system", "content": self.instructions})

        self.search_tools_description = {
            "type": "function",
            "function": {
                "name": "search_tools",
                "description": (
                    "Search for appropriate tools and make them available. "
                    "Note that you may run this function multiple times to search for various functions."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "problem_description": {
                            "type": "string",
                            "description": "A textual description of what you want to achieve.",
                        },
                    },
                    "required": ["problem_description"],
                },
            }
        }

    def search_tools(self, problem_description: str):
        res = self.tool_library.search(
            problem_description=problem_description,
            top_k=self.top_k_functions
        )["documents"][0]
        json_res = [json.loads(e) for e in res]
        logging.info(f"Functions for `{problem_description}`: {json.dumps(json_res)}")
        return json_res

    def __get_response(
        self,
        msgs: list[dict[str, str]],
        model: str = None,
        temperature: float = None,
        tools: list = None,
        tool_choice: str = "auto",
    ):
        response = None
        while not response:
            try:
                response = self.openai_client.chat.completions.create(
                    model=model if model else self.model,
                    messages=msgs,
                    tools=tools,
                    temperature=temperature if temperature else self.temperature,
                    tool_choice=tool_choice if tools else "none",
                )
            except OpenAIError as e:
                logger.error(e)
        return response

    def query(
        self,
        prompt: str,
    ) -> str:
        logging.info(f"Query: {prompt}")
        self.messages.append({"role": "user", "content": prompt})

        # get functions - note that this is not tracked in the message history
        function_response = self.__get_response(
            msgs=self.messages,
            tools=[self.search_tools_description],
            tool_choice={"type": "function", "function": {"name": "search_tools"}},
        )
        response_message = function_response.choices[0].message
        tool_calls = response_message.tool_calls

        tools = []
        for tool_call in tool_calls:
            func = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            assert func == "search_tools", f"Unexpected tool call: {func}"

            # search tulip for function with args
            logging.info(f"Tool search for: {str(args)}")
            tools_ = self.search_tools(**args)
            logging.info(f"Tools found: {str(tools_)}")
            tools.extend(tools_)

        # run with relevant tools
        response = self.__get_response(
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
                    function_name=func_name,
                    function_args=func_args
                )
                self.messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": str(function_response),
                    }
                )
                logger.info(f"Function returned `{str(function_response)}`.")

            response = self.__get_response(
                msgs=self.messages,
                tools=tools,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
        return response_message.content
