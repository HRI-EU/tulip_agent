#!/usr/bin/env python3
"""
A basic agent with function calling capabilities.
"""
import json
import logging

from typing import Callable

from openai import OpenAI, OpenAIError

from constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from function_analyzer import FunctionAnalyzer
from prompts import BASE_PROMPT


logger = logging.getLogger(__name__)


class BaseAgent:
    def __init__(
        self,
        functions: list[Callable],
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.instructions = BASE_PROMPT
        self.openai_client = OpenAI()
        self.function_analyzer = FunctionAnalyzer()

        self.messages = []
        if self.instructions:
            self.messages.append({"role": "system", "content": self.instructions})

        self.tools = {f.__name__: f for f in functions}
        self.tool_descriptions = [
            self.function_analyzer.analyze_function(f) for f in functions
        ]

    def _get_response(
        self,
        msgs: list[dict[str, str]],
        model: str = None,
        temperature: float = None,
    ):
        response = None
        while not response:
            try:
                response = self.openai_client.chat.completions.create(
                    model=model if model else self.model,
                    messages=msgs,
                    tools=self.tool_descriptions,
                    temperature=temperature if temperature else self.temperature,
                    tool_choice="auto" if self.tools else "none",
                )
            except OpenAIError as e:
                logger.error(e)
        logger.info(
            f"Usage for {response.id} in tokens: "
            f"{response.usage.prompt_tokens} prompt and {response.usage.completion_tokens} completion."
        )
        return response

    def query(
        self,
        prompt: str,
    ) -> str:
        logging.info(f"Query: {prompt}")
        self.messages.append({"role": "user", "content": prompt})
        response = self._get_response(
            msgs=self.messages,
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        while tool_calls:
            self.messages.append(response_message)

            for tool_call in tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                function_response = self.tools[func_name](**func_args)
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
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
        self.messages.append(response_message)
        return response_message.content
