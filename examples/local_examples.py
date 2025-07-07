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
Example for using a ToolLibrary and CotTulipAgent with local models.
Assumes that environment variables are set and that the following models are available:
* language model: llama3.2, e.g., https://ollama.com/library/llama3.2
* embedding model: mxbai-embed-large, e.g., https://ollama.com/library/mxbai-embed-large
"""
import logging

from tulip_agent import (
    BaseAgent,
    CotTulipAgent,
    ModelServeMode,
    ToolLibrary,
    create_client,
)


# Set logger to INFO to show agents' internal steps
logging.basicConfig(level=logging.INFO)

tasks = ["""Add 2 and 5""", """Add the product of 3 and 4 and the product of 5 and 6"""]

ba = BaseAgent(model_serve_mode=ModelServeMode.OAI_COMPATIBLE, model="llama3.2")

tulip = ToolLibrary(
    chroma_sub_dir="local_example/",
    file_imports=[("calculator", [])],
    embedding_model="mxbai-embed-large",
    embedding_client=create_client(model_serve_mode=ModelServeMode.OAI_COMPATIBLE),
)
cta = CotTulipAgent(
    tool_library=tulip,
    top_k_functions=3,
    model_serve_mode=ModelServeMode.OAI_COMPATIBLE,
    model="llama3.2",
)

for task in tasks:
    print(f"{task=}")
    ba_res = ba.query(prompt=task)
    print(f"{ba_res=}")
    cta_res = cta.query(prompt=task)
    print(f"{cta_res=}")
