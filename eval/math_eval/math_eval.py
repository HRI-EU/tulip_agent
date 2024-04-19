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
TulipAgent evals
* Models: smaller OpenAI model, gpt-4-turbo
* Datasets: use some Python lib from which I can extract functions? must adhere to Sphinx doc style; or generate
* Several runs, with an increasing number of functions
"""
import json
import logging.config
import yaml

from inspect import getmembers, isfunction

from tulip_agent import (
    AutoTulipAgent,
    BaseAgent,
    MinimalTulipAgent,
    NaiveTulipAgent,
    ToolAgent,
    ToolCotAgent,
    ToolLibrary,
    TulipCotAgent,
)
import math_tools


# Set up agent loggers to save logs to file for analysis
with open("logging_config.yaml", "rt") as log_config:
    config = yaml.safe_load(log_config.read())
logging.config.dictConfig(config)


def run_math_eval(task_file: str):
    functions = [
        getattr(math_tools, n)
        for n, f in getmembers(math_tools, isfunction)
        if f.__module__ == math_tools.__name__
    ]
    print(f"{functions=}")

    with open(task_file, "r") as gtf:
        tasks_ = json.load(gtf)
        queries = {e["task"]: e for e in tasks_}

    for query in queries:
        print(query)

        print(" BASE ".center(40, "="))
        base_agent = BaseAgent()
        base_res = base_agent.query(query)
        print(f"{base_res=}")

        print(" TOOL ".center(40, "="))
        tool_agent = ToolAgent(functions=functions)
        tool_res = tool_agent.query(query)
        print(f"{tool_res=}")

        print(" TOOL COT ".center(40, "="))
        tool_cot_agent = ToolCotAgent(functions=functions)
        tool_cot_res = tool_cot_agent.query(query)
        print(f"{tool_cot_res=}")

        tulip = ToolLibrary(
            chroma_sub_dir="math_eval/",
            file_imports=[("math_tools", [])],
            chroma_base_dir="../../data/chroma/",
        )

        print(" MINIMAL TULIP ".center(40, "="))
        minimal_tulip_agent = MinimalTulipAgent(
            tool_library=tulip,
            top_k_functions=2,
        )
        tulip_res = minimal_tulip_agent.query(query)
        print(f"{tulip_res=}")

        print(" NAIVE TULIP ".center(40, "="))
        naive_tulip_agent = NaiveTulipAgent(
            tool_library=tulip,
            top_k_functions=4,
        )
        tulip_res = naive_tulip_agent.query(query)
        print(f"{tulip_res=}")

        print(" TULIP COT ".center(40, "="))
        tulip_cot_agent = TulipCotAgent(
            tool_library=tulip,
            top_k_functions=3,
        )
        tulip_res = tulip_cot_agent.query(query)
        print(f"{tulip_res=}")

        print(" AUTO TULIP ".center(40, "="))
        auto_tulip_agent = AutoTulipAgent(
            tool_library=tulip,
            top_k_functions=1,
        )
        tulip_res = auto_tulip_agent.query(query)
        print(f"{tulip_res=}")


if __name__ == "__main__":
    run_math_eval(task_file="math_tasks.json")
