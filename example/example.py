#!/usr/bin/env python3
from tulip import (
    BaseAgent,
    ToolLibrary,
    TulipAgent,
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
    b = BaseAgent(
        functions=FUNCTIONS
    )
    return b


def run_comparison():
    query = "What is 45342 * 23487 + 32478?"
    print(query)

    print("="*10 + "BASE" + "="*10)
    base_agent = BaseAgent(functions=FUNCTIONS)
    base_res = base_agent.query(query)
    print(f"{base_res=}")

    print("="*10 + "TULIP" + "="*10)
    tulip = ToolLibrary(functions=FUNCTIONS)
    tulip_agent = TulipAgent(
        tool_library=tulip,
        top_k_functions=1,
    )
    tulip_res = tulip_agent.query(query)
    print(f"{tulip_res=}")


if __name__ == "__main__":
    run_comparison()
