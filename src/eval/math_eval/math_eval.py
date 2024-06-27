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
    InformedCotTulipAgent,
    MinimalTulipAgent,
    NaiveToolAgent,
    NaiveTulipAgent,
    OneShotCotTulipAgent,
    PrunedCotTulipAgent,
    ToolLibrary,
)


# Set up agent loggers to save logs to file for analysis
with open("logging_config.yaml", "rt") as log_config:
    config = yaml.safe_load(log_config.read())
logging.config.dictConfig(config)


# Import tools as specified in settings
with open("math_eval_settings.yaml", "rt") as mes:
    SETTINGS = yaml.safe_load(mes.read())
TOOLS_FILENAME = SETTINGS["tools"]
tools = importlib.import_module(TOOLS_FILENAME)


def run_math_eval(
    task_file: str,
    agents: list[str],
    task_filter: list[str],
    model: str,
    embedding_model: str,
    number_of_runs: int,
    log_file: str,
    tulip_top_k: int,
    search_similarity_threshold: float,
):
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
        chroma_sub_dir=f"math_eval_{embedding_model}/",
        file_imports=[(TOOLS_FILENAME, [])],
        chroma_base_dir="../../../data/chroma/",
        embedding_model=embedding_model,
    )

    def _run(agent_class, setup_args: dict) -> None:
        print(f" {agent_class.__name__} ".center(40, "="))
        for r in range(number_of_runs):
            for query in queries:
                if task_filter and queries[query]["name"] not in task_filter:
                    continue
                agent = agent_class(**setup_args)
                print(
                    f"{agent_class.__name__} -- {queries[query]['name']} -- {query} -- run [{r+1}/{number_of_runs}]"
                )
                res = agent.query(query)
                print(f"{res=}")
            shutil.copy("math.eval.log", log_file)

    if "BaseAgent" in agents:
        _run(
            agent_class=BaseAgent,
            setup_args={"model": model},
        )

    for agent_class in (NaiveToolAgent, CotToolAgent):
        if agent_class.__name__ in agents:
            _run(
                agent_class=agent_class,
                setup_args={"model": model, "functions": functions},
            )

    for agent_class in (
        MinimalTulipAgent,
        NaiveTulipAgent,
        CotTulipAgent,
        InformedCotTulipAgent,
        PrunedCotTulipAgent,
        OneShotCotTulipAgent,
        AutoTulipAgent,
    ):
        if agent_class.__name__ in agents:
            _run(
                agent_class=agent_class,
                setup_args={
                    "model": model,
                    "tool_library": tulip,
                    "top_k_functions": tulip_top_k,
                    "search_similarity_threshold": search_similarity_threshold,
                    "api_interaction_limit": 50,
                },
            )


def main():
    # back up log
    log_folder = SETTINGS["log_folder"]
    Path(log_folder).mkdir(parents=True, exist_ok=True)
    log_name = "math.eval." + datetime.now().strftime("%Y%m%d-%H%M") + ".log"
    log_file = f"{log_folder}/{log_name}"
    # run
    number_of_runs = SETTINGS["number_of_runs"]
    run_math_eval(
        task_file=SETTINGS["ground_truth"],
        agents=[a for a in SETTINGS["agents"] if SETTINGS["agents"][a]],
        task_filter=SETTINGS["task_filter"],
        model=SETTINGS["model"],
        embedding_model=SETTINGS["embedding_model"],
        number_of_runs=number_of_runs,
        log_file=log_file,
        tulip_top_k=SETTINGS["tulip_top_k"],
        search_similarity_threshold=SETTINGS["search_similarity_threshold"],
    )
    # track settings
    if os.path.exists((history_path := log_folder + "/history.json")):
        with open(history_path, "r") as h:
            history = json.load(h)
    else:
        history = {}
    history[log_name] = SETTINGS
    with open(history_path, "w") as h:
        json.dump(history, h, indent=4)


if __name__ == "__main__":
    main()
