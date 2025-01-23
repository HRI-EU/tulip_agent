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
MinimalTulipAgent variant.
"""
import logging
from typing import Optional

from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from tulip_agent.prompts import TOOL_PROMPT
from tulip_agent.tool_library import ToolLibrary

from .llm_agent import ModelServeMode
from .tulip_agent import TulipAgent


logger = logging.getLogger(__name__)


class MinimalTulipAgent(TulipAgent):
    def __init__(
        self,
        model: str = BASE_LANGUAGE_MODEL,
        temperature: float = BASE_TEMPERATURE,
        model_serve_mode: ModelServeMode = ModelServeMode.OPENAI,
        api_interaction_limit: int = 100,
        tool_library: ToolLibrary = None,
        top_k_functions: int = 10,
        search_similarity_threshold: float = None,
        instructions: Optional[str] = None,
    ) -> None:
        super().__init__(
            instructions=(
                TOOL_PROMPT + "\n\n" + instructions if instructions else TOOL_PROMPT
            ),
            model=model,
            temperature=temperature,
            model_serve_mode=model_serve_mode,
            api_interaction_limit=api_interaction_limit,
            tool_library=tool_library,
            top_k_functions=top_k_functions,
            search_similarity_threshold=search_similarity_threshold,
        )

    def query(
        self,
        prompt: str,
    ) -> str:
        logger.info(f"{self.__class__.__name__} received query: {prompt}")

        # Search for tools directly with user prompt; do not track the search
        tools = self.search_tools(
            action_descriptions=[prompt],
            similarity_threshold=self.search_similarity_threshold,
        )[0][1]

        # Run with tools
        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        response = self.run_with_tools(tools=tools)
        logger.info(f"{self.__class__.__name__} returns response: {response}")
        return response
