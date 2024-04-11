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

    print_seperator(name=BaseAgent.__name__)
    base_agent = BaseAgent()
    base_res = base_agent.query(query)
    print(f"{base_res=}")

    for agent_type in (ToolAgent, ToolCotAgent):
        print_seperator(name=agent_type.__name__)
        agent = agent_type(functions=FUNCTIONS)
        res = agent.query(query)
        print(f"{res=}")

    tulip = ToolLibrary(chroma_sub_dir="example/", functions=FUNCTIONS)

    type_k_combinations = (
        (MinimalTulipAgent, 2),
        (NaiveTulipAgent, 4),
        (TulipCotAgent, 1),
        (AutoTulipAgent, 1),
    )
    for agent_type, top_k in type_k_combinations:
        print_seperator(name=agent_type.__name__)
        tulip_agent = agent_type(
            tool_library=tulip,
            top_k_functions=top_k,
        )
        res = tulip_agent.query(query)
        print(f"{res=}")


if __name__ == "__main__":
    run_comparison()
