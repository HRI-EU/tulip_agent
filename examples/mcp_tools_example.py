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
import logging
from pathlib import Path

from tulip_agent import MinimalTulipAgent, ToolLibrary


logging.basicConfig(level=logging.ERROR)


tasks = [
    "Summarize the contents of the github repo `HRI-EU/tulip_agent` in one sentence.",
    "What is 12 * 289?",
    "Add 12 and 289.",
    "How many files are in the current directory?",
]


tulip = ToolLibrary(
    chroma_sub_dir="example_mcp_tools/",
    mcp_imports=[
        (
            {
                "mcpServers": {
                    # remote MCP server
                    "deepwiki": {
                        "url": "https://mcp.deepwiki.com/mcp",
                        "transport": "http",
                    },
                    # local, up-and-running MCP server
                    "multiplication": {
                        "url": "http://127.0.0.2:8000/mcp",
                        "transport": "http",
                    },
                    # local file with an MCP server, not running
                    "addition": {
                        "command": "python",
                        "args": [str(Path(__file__).parent / "example_mcp_add.py")],
                        "transport": "stdio",
                    },
                    # MCP server as a package
                    "filesystem": {
                        "command": "uvx",
                        "args": ["fastmcp-file-server"],
                        "transport": "stdio",
                        "env": {
                            "MCP_ALLOWED_PATH": str(
                                Path(__file__).parent.resolve().absolute()
                            ),
                        },
                    },
                }
            },
            [],
        )
    ],
)
print(tulip.tools)
agent = MinimalTulipAgent(
    base_model="gpt-5.2",
    tool_library=tulip,
    top_k_functions=2,
)

for task in tasks:
    print(f"{task=}")
    res = agent.query(prompt=task)
    print(f"{res=}")
