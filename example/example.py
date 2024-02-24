#!/usr/bin/env python3
from tulip import ToolLibrary
from tulip import TulipAgent
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


def init_tulip():
    tulip = ToolLibrary(
        functions=[
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
    )
    return tulip


if __name__ == "__main__":
    tulip = init_tulip()
    tulip_agent = TulipAgent(
        tool_library=tulip,
        top_k_functions=3,
    )
    query = "What is 45342 * 23487 + 32478?"
    print(query)
    res = tulip_agent.query(query)
    print(res)