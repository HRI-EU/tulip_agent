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
Basic LLM agent.
"""
import logging

from abc import ABC, abstractmethod
from typing import Optional

from openai import OpenAI, OpenAIError

from .constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from .prompts import BASE_PROMPT


logger = logging.getLogger(__name__)


class LlmAgent(ABC):
    def __init__(
        self,
        instructions: str,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.instructions = instructions
        self.openai_client = OpenAI()

        self.messages = []
        if self.instructions:
            self.messages.append({"role": "system", "content": self.instructions})

    def _get_response(
        self,
        msgs: list[dict[str, str]],
        tools: list = None,
        tool_choice: str = "auto",
        model: str = None,
        temperature: float = None,
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
        Query the agent.

        :param prompt: User prompt
        :return: User-oriented final response
        """
        pass


class BaseAgent(LlmAgent):
    def __init__(
        self,
        instructions: Optional[str] = None,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
    ) -> None:
        super().__init__(
            instructions=(
                BASE_PROMPT + "\n\n" + instructions if instructions else BASE_PROMPT
            ),
            model=model,
            temperature=temperature,
        )

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