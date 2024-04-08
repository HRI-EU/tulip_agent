#!/usr/bin/env python3
import logging

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
from calculator import (
    add,
    subtract,
    multiply,
    divide,
    square_root,
    exponent,
    modulus,
    sine,
    cosine,
    tangent,
)


# Set logger to INFO to show agents' internal steps
logging.basicConfig(level=logging.INFO)


FUNCTIONS = [
    add,
    subtract,
    multiply,
    divide,
    square_root,
    exponent,
    modulus,
    sine,
    cosine,
    tangent,
]


def print_seperator(name: str) -> None:
    print("=" * 10 + f" {name} " + "=" * 10)


def run_comparison():
    query = "What is 45342 * 23487 + 32478?"
    print(query)

    print_seperator(name="BASE")
    base_agent = BaseAgent()
    base_res = base_agent.query(query)
    print(f"{base_res=}")

    print_seperator(name="TOOL")
    tool_agent = ToolAgent(functions=FUNCTIONS)
    tool_res = tool_agent.query(query)
    print(f"{tool_res=}")

    print_seperator(name="TOOL COT")
    tool_cot_agent = ToolCotAgent(functions=FUNCTIONS)
    tool_cot_res = tool_cot_agent.query(query)
    print(f"{tool_cot_res=}")

    tulip = ToolLibrary(chroma_sub_dir="example/", functions=FUNCTIONS)

    print_seperator(name="MINIMAL TULIP")
    minimal_tulip_agent = MinimalTulipAgent(
        tool_library=tulip,
        top_k_functions=2,
    )
    tulip_res = minimal_tulip_agent.query(query)
    print(f"{tulip_res=}")

    print_seperator(name="NAIVE TULIP")
    naive_tulip_agent = NaiveTulipAgent(
        tool_library=tulip,
        top_k_functions=4,
    )
    tulip_res = naive_tulip_agent.query(query)
    print(f"{tulip_res=}")

    print_seperator(name="TULIP COT")
    tulip_cot_agent = TulipCotAgent(
        tool_library=tulip,
        top_k_functions=1,
    )
    tulip_res = tulip_cot_agent.query(query)
    print(f"{tulip_res=}")

    print_seperator(name="AUTO TULIP")
    auto_tulip_agent = AutoTulipAgent(
        tool_library=tulip,
        top_k_functions=1,
    )
    tulip_res = auto_tulip_agent.query(query)
    print(f"{tulip_res=}")


if __name__ == "__main__":
    run_comparison()
