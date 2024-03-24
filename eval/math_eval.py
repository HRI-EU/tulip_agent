#!/usr/bin/env python3
"""
TulipAgent evals
* Models: smaller OpenAI model, gpt-4-turbo
* Datasets: use some Python lib from which I can extract functions? must adhere to Sphinx doc style; or generate
* Several runs, with an increasing number of functions
"""
import logging.config
import yaml

from inspect import getmembers, isfunction

from tulip import (
    ToolAgent,
    ToolLibrary,
    TulipCotAgent,
)
import math_tools


# Set up agent loggers to save logs to file for analysis
with open("logging_config.yaml", "rt") as log_config:
    config = yaml.safe_load(log_config.read())
logging.config.dictConfig(config)


def run_math_eval():
    functions = [
        getattr(math_tools, n)
        for n, f in getmembers(math_tools, isfunction)
        if f.__module__ == math_tools.__name__
    ]
    print(functions)

    queries = [
        "What is 45342 * 23487 + 32478?",  # 1064980032
        "What is the variation coefficient for 1, 2, and 3?",  # 0.408
    ]

    for query in queries:
        print(query)

        print("=" * 10 + " TOOL " + "=" * 10)
        tool_agent = ToolAgent(functions=functions)
        tool_res = tool_agent.query(query)
        print(f"{tool_res=}")

        print("=" * 10 + " TULIP COT " + "=" * 10)
        tulip = ToolLibrary(chroma_sub_dir="math_eval/", functions=functions)
        tulip_cot_agent = TulipCotAgent(
            tool_library=tulip,
            top_k_functions=3,
        )
        tulip_res = tulip_cot_agent.query(query)
        print(f"{tulip_res=}")


if __name__ == "__main__":
    run_math_eval()
