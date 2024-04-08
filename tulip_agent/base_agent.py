#!/usr/bin/env python3
"""
Several agent variations as a baseline; with and without tool access.
"""
import json
import logging

from abc import ABC, abstractmethod
from typing import Callable

from openai import OpenAI, OpenAIError

from .constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from .function_analyzer import FunctionAnalyzer
from .prompts import (
    BASE_PROMPT,
    SOLVE_WITH_TOOLS,
    TASK_DECOMPOSITION,
    TOOL_COT_PROMPT,
    TOOL_PROMPT,
)


logger = logging.getLogger(__name__)


class ToolBaseAgent(ABC):
    def __init__(
        self,
        instructions: str,
        functions: list[Callable],
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.instructions = instructions
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
        tool_choice: str = None,
    ):
        response = None
        if tool_choice:
            tool_choice_ = tool_choice
        elif self.tools:
            tool_choice_ = "auto"
        else:
            tool_choice_ = "none"
        while not response:
            try:
                response = self.openai_client.chat.completions.create(
                    model=model if model else self.model,
                    messages=msgs,
                    tools=self.tool_descriptions,
                    temperature=temperature if temperature else self.temperature,
                    tool_choice=tool_choice_,
                )
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
        Query the tool agent, which has to figure out which tools to use.

        :param prompt: User prompt
        :return: User-oriented final response
        """
        pass

    def run_with_tools(self):
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
        logger.info(
            f"{self.__class__.__name__} returns response: {response_message.content}"
        )
        return response_message.content


class BaseAgent:
    def __init__(
        self,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.instructions = BASE_PROMPT
        self.openai_client = OpenAI()

        self.messages = []
        if self.instructions:
            self.messages.append({"role": "system", "content": self.instructions})

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
                    temperature=temperature if temperature else self.temperature,
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
        logger.info(f"{self.__class__.__name__} received query: {prompt}")
        self.messages.append({"role": "user", "content": prompt})
        response = self._get_response(
            msgs=self.messages,
        )
        response_message = response.choices[0].message
        self.messages.append(response_message)
        logger.info(
            f"{self.__class__.__name__} returns response: {response_message.content}"
        )
        return response_message.content


class ToolAgent(ToolBaseAgent):
    def __init__(
        self,
        functions: list[Callable],
        instructions: str = TOOL_PROMPT,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
    ) -> None:
        super().__init__(
            instructions=instructions,
            functions=functions,
            model=model,
            temperature=temperature,
        )

    def query(
        self,
        prompt: str,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")
        self.messages.append({"role": "user", "content": prompt})
        return self.run_with_tools()


class ToolCotAgent(ToolBaseAgent):
    def __init__(
        self,
        functions: list[Callable],
        instructions: str = TOOL_COT_PROMPT,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
    ) -> None:
        super().__init__(
            instructions=instructions,
            functions=functions,
            model=model,
            temperature=temperature,
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
            tool_choice="none",
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