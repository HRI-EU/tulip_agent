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
import json
import logging.config
import os.path
import shutil
import yaml

from datetime import datetime
from inspect import getmembers, isfunction
from pathlib import Path

from tulip_agent import (
    AutoTulipAgent,
    BaseAgent,
    MinimalTulipAgent,
    NaiveTulipAgent,
    NaiveToolAgent,
    CotToolAgent,
    ToolLibrary,
    CotTulipAgent,
)
import math_tools


# Set up agent loggers to save logs to file for analysis
with open("logging_config.yaml", "rt") as log_config:
    config = yaml.safe_load(log_config.read())
logging.config.dictConfig(config)


def run_math_eval(task_file: str, agents: list[str]):
    functions = [
        getattr(math_tools, n)
        for n, f in getmembers(math_tools, isfunction)
        if f.__module__ == math_tools.__name__
    ]
    print(f"{functions=}")

    with open(task_file, "r") as gtf:
        tasks_ = json.load(gtf)
        queries = {e["task"]: e for e in tasks_}

    tulip = ToolLibrary(
        chroma_sub_dir="math_eval/",
        file_imports=[("math_tools", [])],
        chroma_base_dir="../../../data/chroma/",
    )

    def _run(agent) -> None:
        for query in queries:
            print(queries[query]["name"], "--", query)
            res = agent.query(query)
            print(f"{res=}")

    if "BaseAgent" in agents:
        print(" BaseAgent ".center(40, "="))
        agent = BaseAgent()
        _run(agent)

    if "NaiveToolAgent" in agents:
        print(" NaiveToolAgent ".center(40, "="))
        agent = NaiveToolAgent(functions=functions)
        _run(agent)

    if "CotToolAgent" in agents:
        print(" CotToolAgent ".center(40, "="))
        agent = CotToolAgent(functions=functions)
        _run(agent)

    if "MinimalTulipAgent" in agents:
        print(" MinimalTulipAgent ".center(40, "="))
        agent = MinimalTulipAgent(
            tool_library=tulip,
            top_k_functions=5,
        )
        _run(agent)

    if "NaiveTulipAgent" in agents:
        print(" NaiveTulipAgent ".center(40, "="))
        agent = NaiveTulipAgent(
            tool_library=tulip,
            top_k_functions=5,
        )
        _run(agent)

    if "CotTulipAgent" in agents:
        print(" CotTulipAgent ".center(40, "="))
        agent = CotTulipAgent(
            tool_library=tulip,
            top_k_functions=5,
        )
        _run(agent)

    if "AutoTulipAgent" in agents:
        print(" AutoTulipAgent ".center(40, "="))
        agent = AutoTulipAgent(
            tool_library=tulip,
            top_k_functions=5,
        )
        _run(agent)


def main():
    with open("math_eval_settings.yaml", "rt") as mes:
        settings = yaml.safe_load(mes.read())
    run_math_eval(
        task_file=settings["ground_truth"],
        agents=[a for a in settings["agents"] if settings["agents"][a]],
    )
    # back up log
    log_folder = settings["log_folder"]
    log_name = "math.eval." + datetime.now().strftime("%Y%m%d-%H%M") + ".log"
    Path(log_folder).mkdir(parents=True, exist_ok=True)
    shutil.copy("math.eval.log", f"{log_folder}/{log_name}")
    # track settings
    if os.path.exists((history_path := log_folder + "/history.json")):
        with open(history_path, "r") as h:
            history = json.load(h)
    else:
        history = {}
    history[log_name] = settings
    with open(history_path, "w") as h:
        json.dump(history, h, indent=4)


if __name__ == "__main__":
    main()
