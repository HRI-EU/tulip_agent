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
import importlib
import json
import logging.config
import os.path
import shutil
from datetime import datetime
from inspect import getmembers, isfunction
from pathlib import Path

import yaml
from tulip_agent import (
    AutoTulipAgent,
    BaseAgent,
    CotToolAgent,
    CotTulipAgent,
    MinimalTulipAgent,
    NaiveToolAgent,
    NaiveTulipAgent,
    ToolLibrary,
)
from tulip_agent.constants import BASE_LANGUAGE_MODEL


# Set up agent loggers to save logs to file for analysis
with open("logging_config.yaml", "rt") as log_config:
    config = yaml.safe_load(log_config.read())
logging.config.dictConfig(config)


# Import tools as specified in settings
with open("math_eval_settings.yaml", "rt") as mes:
    SETTINGS = yaml.safe_load(mes.read())
TOOLS_FILENAME = SETTINGS["tools"]
tools = importlib.import_module(TOOLS_FILENAME)


def run_math_eval(task_file: str, agents: list[str], task_filter: list[str]):
    functions = [
        getattr(tools, n)
        for n, f in getmembers(tools, isfunction)
        if f.__module__ == tools.__name__
    ]
    print(f"{functions=}")

    with open(task_file, "r") as gtf:
        tasks_ = json.load(gtf)
        queries = {e["task"]: e for e in tasks_}

    tulip = ToolLibrary(
        chroma_sub_dir="math_eval/",
        file_imports=[(TOOLS_FILENAME, [])],
        chroma_base_dir="../../../data/chroma/",
    )

    def _run(agent_class, setup_args: dict) -> None:
        print(f" {agent_class.__name__} ".center(40, "="))
        for query in queries:
            if task_filter and queries[query]["name"] not in task_filter:
                continue
            agent = agent_class(**setup_args)
            print(agent_class.__name__, "--", queries[query]["name"], "--", query)
            res = agent.query(query)
            print(f"{res=}")

    if "BaseAgent" in agents:
        _run(agent_class=BaseAgent, setup_args={})

    if "NaiveToolAgent" in agents:
        _run(agent_class=NaiveToolAgent, setup_args={"functions": functions})

    if "CotToolAgent" in agents:
        _run(agent_class=CotToolAgent, setup_args={"functions": functions})

    if "MinimalTulipAgent" in agents:
        _run(
            agent_class=MinimalTulipAgent,
            setup_args={"tool_library": tulip, "top_k_functions": 5},
        )

    if "NaiveTulipAgent" in agents:
        _run(
            agent_class=NaiveTulipAgent,
            setup_args={"tool_library": tulip, "top_k_functions": 5},
        )

    if "CotTulipAgent" in agents:
        _run(
            agent_class=CotTulipAgent,
            setup_args={"tool_library": tulip, "top_k_functions": 5},
        )

    if "AutoTulipAgent" in agents:
        _run(
            agent_class=AutoTulipAgent,
            setup_args={"tool_library": tulip, "top_k_functions": 5},
        )


def main():
    run_math_eval(
        task_file=SETTINGS["ground_truth"],
        agents=[a for a in SETTINGS["agents"] if SETTINGS["agents"][a]],
        task_filter=SETTINGS["task_filter"],
    )
    # back up log
    log_folder = SETTINGS["log_folder"]
    log_name = "math.eval." + datetime.now().strftime("%Y%m%d-%H%M") + ".log"
    Path(log_folder).mkdir(parents=True, exist_ok=True)
    shutil.copy("math.eval.log", f"{log_folder}/{log_name}")
    # track settings
    if os.path.exists((history_path := log_folder + "/history.json")):
        with open(history_path, "r") as h:
            history = json.load(h)
    else:
        history = {}
    history[log_name] = SETTINGS
    history[log_name]["model"] = BASE_LANGUAGE_MODEL
    with open(history_path, "w") as h:
        json.dump(history, h, indent=4)


if __name__ == "__main__":
    main()
