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
import unittest

from tests.example_tools_in_class import Calculator
from tulip_agent import (
    AutoTulipAgent,
    CotTulipAgent,
    DfsTulipAgent,
    InformedCotTulipAgent,
    MinimalTulipAgent,
    NaiveTulipAgent,
    OneShotCotTulipAgent,
    PrimedCotTulipAgent,
    ToolLibrary,
)


class TestTulipAgent(unittest.TestCase):

    def setUp(self):
        self.tulip = ToolLibrary(chroma_sub_dir="test/")
        self.tulip.chroma_client.delete_collection("tulip")
        self.tulip = ToolLibrary(
            chroma_sub_dir="test/",
            file_imports=[("tests.example_tools", [])],
            description="Various math tools.",
        )

    @staticmethod
    def _tool_message_names(messages: list) -> list[str]:
        return [
            message["name"]
            for message in messages
            if isinstance(message, dict) and message.get("role") == "tool"
        ]

    def _check_res(self, res: str, messages: list):
        tool_message_names = self._tool_message_names(messages)
        self.assertTrue(
            any(s in res.lower() for s in ("4", "four"))
            and "add" in tool_message_names,
            "LLM query failed.",
        )

    def test_naive_tulip_query(self):
        agent = NaiveTulipAgent(tool_library=self.tulip)
        res = agent.query(prompt="What is 2+2?")
        self._check_res(res, agent.messages)

    def test_minimal_tulip_query(self):
        agent = MinimalTulipAgent(tool_library=self.tulip)
        res = agent.query(prompt="What is 2+2?")
        self._check_res(res, agent.messages)

    def test_cot_tulip_query(self):
        agent = CotTulipAgent(tool_library=self.tulip)
        res = agent.query(prompt="What is 2+2?")
        self._check_res(res, agent.messages)

    def test_informed_cot_tulip_query(self):
        agent = InformedCotTulipAgent(tool_library=self.tulip)
        res = agent.query(prompt="What is 2+2?")
        self._check_res(res, agent.messages)

    def test_one_shot_cot_tulip_query(self):
        agent = OneShotCotTulipAgent(tool_library=self.tulip)
        res = agent.query(prompt="What is 2+2?")
        self._check_res(res, agent.messages)

    def test_primed_cot_tulip_query(self):
        agent = PrimedCotTulipAgent(tool_library=self.tulip)
        res = agent.query(prompt="What is 2+2?")
        self._check_res(res, agent.messages)

    def test_dfs_tulip_query(self):
        agent = DfsTulipAgent(tool_library=self.tulip)
        res = agent.query(prompt="What is 2+2?")
        self.assertTrue(
            any(s in res.lower() for s in ("4", "four"))
            and len(agent.task.tool_candidates) == 2
            and "add" in [tc.unique_id for tc in agent.task.tool_candidates],
            "LLM query failed.",
        )

    def test_auto_tulip_query(self):
        agent = AutoTulipAgent(tool_library=self.tulip)
        res = agent.query(prompt="What is 2+2?")
        self.assertTrue(
            any(s in res.lower() for s in ("4", "four")),
            "LLM query failed.",
        )

    def test_cot_tulip_query_with_instance(self):
        calculator = Calculator(divisor=3)
        self.tulip.chroma_client.delete_collection("tulip")
        self.tulip = ToolLibrary(
            chroma_sub_dir="test/",
            instance_imports=[calculator],
            description="Various math tools.",
        )
        agent = CotTulipAgent(tool_library=self.tulip)
        res = agent.query(prompt="What is 2+2?")
        tool_message_names = self._tool_message_names(agent.messages)
        self.assertTrue(
            any(s in res.lower() for s in ("4", "four"))
            and "add" in tool_message_names,
            "LLM query failed.",
        )

    def test_default_tools(self):
        character = (
            "You must solve the task provided by the user using a tool. "
            "Eventually use the speak function to tell them the result."
        )
        agent = MinimalTulipAgent(
            tool_library=self.tulip,
            default_tools=[self.tulip.tools["speak"]],
            top_k_functions=1,
            instructions=character,
        )
        res = agent.query(prompt="What is 2+2?")
        tool_message_names = self._tool_message_names(agent.messages)
        self.assertTrue(
            any(s in res.lower() for s in ("4", "four"))
            and "speak" in tool_message_names,
            "Using default_tool failed.",
        )


if __name__ == "__main__":
    unittest.main()
