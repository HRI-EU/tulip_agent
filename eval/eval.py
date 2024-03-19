#!/usr/bin/env python3
"""
TulipAgent evals
* Models: smaller OpenAI model, gpt-4-turbo
* Datasets: use some Python lib from which I can extract functions? must adhere to Sphinx doc style; or generate
* Several runs, with an increasing number of functions
"""
from inspect import getmembers, isfunction

from tulip import (
    BaseAgent,
    ToolLibrary,
    TulipCotAgent,
)
import calculator_extended


def run_math_eval():
    # TODO: support lists as input types in function descriptions

    functions = [
        getattr(calculator_extended, n)
        for n, _ in getmembers(calculator_extended, isfunction)
    ][:10]
    print(functions)

    query = "What is 45342 * 23487 + 32478?"
    print(query)

    print("=" * 10 + " BASE " + "=" * 10)
    base_agent = BaseAgent(functions=functions)
    base_res = base_agent.query(query)
    print(f"{base_res=}")

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
