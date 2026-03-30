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
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

from tulip_agent import tracing


class FakeCall:
    pass


class FakeClient:
    def __init__(self) -> None:
        self.created = []
        self.finished = []

    def create_call(self, **kwargs):
        self.created.append(kwargs)
        return FakeCall()

    def finish_call(self, call, output=None, exception=None):
        self.finished.append(
            {
                "call": call,
                "output": output,
                "exception": exception,
            }
        )


class FakeExecutor(ThreadPoolExecutor):
    pass


class TestTracing(unittest.TestCase):

    def setUp(self):
        tracing.reset_weave_state()

    def tearDown(self):
        tracing.reset_weave_state()

    def test_trace_call_noop_when_disabled(self):
        res = tracing.trace_call(
            "tulip.test",
            lambda: "ok",
            inputs={"prompt": "secret"},
            attributes={"agent_class": "Test"},
        )
        self.assertEqual(res, "ok")
        self.assertFalse(tracing.weave_tracing_enabled())

    def test_trace_call_uses_manual_weave_client(self):
        client = FakeClient()
        tracing._weave_client = client
        tracing._weave_enabled = True
        tracing._weave_init_attempted = True
        tracing._trace_inputs = False

        res = tracing.trace_call(
            "tulip.test",
            lambda: {"value": 4},
            inputs={"prompt": "secret", "count": 1},
            attributes={"agent_class": "Test"},
        )

        self.assertEqual(res, {"value": 4})
        self.assertEqual(len(client.created), 1)
        self.assertEqual(client.created[0]["op"], "tulip.test")
        self.assertEqual(
            client.created[0]["inputs"],
            {"redacted": True, "keys": ["count", "prompt"]},
        )
        self.assertEqual(client.created[0]["attributes"], {"agent_class": "Test"})
        self.assertEqual(client.finished[0]["output"], {"value": 4})
        self.assertIsNone(client.finished[0]["exception"])

    def test_get_thread_pool_executor_prefers_weave_executor(self):
        client = FakeClient()
        tracing._weave_client = client
        tracing._weave_enabled = True
        tracing._weave_init_attempted = True
        tracing._weave_module = SimpleNamespace(ThreadPoolExecutor=FakeExecutor)

        self.assertIs(tracing.get_thread_pool_executor(), FakeExecutor)


if __name__ == "__main__":
    unittest.main()
