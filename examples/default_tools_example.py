#!/usr/bin/env python3
#
#  Copyright (c) 2024-2025, Honda Research Institute Europe GmbH
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  SPDX-License-Identifier: BSD-3-Clause
#
#
"""
`default_tools` can be used to make sure that certain tools are always available, even without searching the library.
This is helpful when a behavior is specified in the system prompt that explicitly mentions certain tools.
When not making sure that the tool is available, this may lead to infinite loops of tool calls in case of gpt-4o series.
Comment out the line that sets `default_tools` in the NaiveTulipAgent to reproduce the issue.
"""
import logging

from tulip_agent import NaiveTulipAgent, ToolLibrary


logging.basicConfig(level=logging.INFO)


tasks = ["Turn the fan on.", "Set the AC to 22 degrees celsius."]

character = """\
You are a helpful home automation bot.

Always adhere to the following procedure:
1. Identify all individual steps mentioned in the user request.
2. Whenever possible use the tools available to fulfill the user request.
3. Respond to the user using the `say_via_speaker` function.
"""

tulip = ToolLibrary(
    chroma_sub_dir="example_default_tools/", file_imports=[("home_automation", [])]
)
agent = NaiveTulipAgent(
    base_model="gpt-4o-mini",
    tool_library=tulip,
    default_tools=[tulip.tools["say_via_speaker"]],
    top_k_functions=1,
    instructions=character,
)

for task in tasks:
    print(f"{task=}")
    res = agent.query(prompt=task)
    print(f"{res=}")
