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
import unittest

from example_tools import add, slow
from tulip_agent import CotToolAgent, NaiveToolAgent


class TestCore(unittest.TestCase):

    def _check_res(self, res: str, messages: list):
        self.assertTrue(
            any(s in res.lower() for s in ("4", "four"))
            and messages[-2]["role"] == "tool"
            and messages[-2]["name"] == "add",
            "LLM query failed.",
        )

    def test_naive_tool_query(self):
        agent = NaiveToolAgent(functions=[add])
        res = agent.query(prompt="What is 2+2?")
        self._check_res(res, agent.messages)

    def test_naive_tool_query_no_tools(self):
        agent = NaiveToolAgent(functions=[])
        res = agent.query(prompt="What is 2+2?")
        self.assertTrue(
            any(s in res.lower() for s in ("4", "four"))
            and agent.tool_descriptions == [],
            "LLM query failed.",
        )

    def test_cot_tool_query(self):
        agent = CotToolAgent(functions=[add])
        res = agent.query(prompt="What is 2+2?")
        self._check_res(res, agent.messages)

    def test_naive_tool_timeout(self):
        agent = NaiveToolAgent(functions=[slow])
        agent.tool_timeout = 1
        _ = agent.query(prompt="Run the slow function with a duration of 10.")
        self.assertEqual(
            "Error: The tool did not return a response within the specified timeout.",
            agent.messages[-2]["content"],
            "Timeout failed.",
        )


if __name__ == "__main__":
    unittest.main()
