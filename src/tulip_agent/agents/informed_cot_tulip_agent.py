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
InformedCotTulipAgent variant; uses a vector store as a tool library, COT for task decomposition,
and is informed about the contents of its tool library.
"""
import logging
from typing import Optional

from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
from tulip_agent.prompts import INFORMED_TASK_DECOMPOSITION, TULIP_COT_PROMPT
from tulip_agent.tool_library import ToolLibrary

from .llm_agent import ModelServeMode
from .cot_tulip_agent import CotTulipAgent


logger = logging.getLogger(__name__)


class InformedCotTulipAgent(CotTulipAgent):
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
        decomposition_prompt: str = INFORMED_TASK_DECOMPOSITION,
    ) -> None:
        super().__init__(
            instructions=(
                TULIP_COT_PROMPT + "\n\n" + instructions
                if instructions
                else TULIP_COT_PROMPT
            ),
            model=model,
            temperature=temperature,
            model_serve_mode=model_serve_mode,
            api_interaction_limit=api_interaction_limit,
            tool_library=tool_library,
            top_k_functions=top_k_functions,
            search_similarity_threshold=search_similarity_threshold,
            decomposition_prompt=decomposition_prompt.replace(
                "{library_description}",
                tool_library.description if tool_library.description else "",
            ),
        )
        if not tool_library.description:
            logger.warning(
                (
                    "No description set for the tool library. "
                    "This is likely to impact the performance of the InformedCotTulipAgent."
                )
            )
