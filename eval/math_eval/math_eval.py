#!/usr/bin/env python3
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

from tulip import (
    AutoTulipAgent,
    BaseAgent,
    MinimalTulipAgent,
    NaiveTulipAgent,
    ToolAgent,
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

        tulip = ToolLibrary(chroma_sub_dir="math_eval/", functions=functions)

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
