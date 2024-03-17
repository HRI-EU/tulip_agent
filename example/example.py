#!/usr/bin/env python3
from tulip import (
    BaseAgent,
    NaiveTulipAgent,
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


def init_base():
    b = BaseAgent(functions=FUNCTIONS)
    return b


def run_comparison():
    query = "What is 45342 * 23487 + 32478?"
    print(query)

    print("=" * 10 + "BASE" + "=" * 10)
    base_agent = BaseAgent(functions=FUNCTIONS)
    base_res = base_agent.query(query)
    print(f"{base_res=}")

    tulip = ToolLibrary(functions=FUNCTIONS)

    print("=" * 10 + "NAIVE TULIP" + "=" * 10)
    naive_tulip_agent = NaiveTulipAgent(
        tool_library=tulip,
        top_k_functions=4,
    )
    tulip_res = naive_tulip_agent.query(query)
    print(f"{tulip_res=}")

    print("=" * 10 + "TULIP COT" + "=" * 10)
    tulip_cot_agent = TulipCotAgent(
        tool_library=tulip,
        top_k_functions=1,
    )
    tulip_res = tulip_cot_agent.query(query)
    print(f"{tulip_res=}")


if __name__ == "__main__":
    run_comparison()
