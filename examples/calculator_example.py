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
import logging

from calculator import (
    add,
    cosine,
    divide,
    exponent,
    modulus,
    multiply,
    sine,
    square_root,
    subtract,
    tangent,
)
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
    PrimedCotTulipAgent,
    ToolLibrary,
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
    # query = "What is 45342 * 23487 + ((32478 - 2) * (-1) + 2)?"  # 1064915080
    query = "Find the value of $x$ such that $\sqrt{x - 2} = 8$."
    print(query)

    print_seperator(name=BaseAgent.__name__)
    base_agent = BaseAgent()
    base_res = base_agent.query(query)
    print(f"{base_res=}")

    for agent_type in (NaiveToolAgent, CotToolAgent):
        print_seperator(name=agent_type.__name__)
        agent = agent_type(functions=FUNCTIONS)
        res = agent.query(query)
        print(f"{res=}")

    tulip = ToolLibrary(
        chroma_sub_dir="example/",
        file_imports=[("calculator", [])],
        description="A tool library containing math tools.",
    )

    type_k_combinations = (
        (MinimalTulipAgent, 5, 2),
        (NaiveTulipAgent, 5, 2),
        (CotTulipAgent, 5, 2),
        (InformedCotTulipAgent, 5, 2),
        (PrimedCotTulipAgent, 5, 2),
        (OneShotCotTulipAgent, 5, 2),
        (AutoTulipAgent, 5, 2),
    )
    for agent_type, top_k, sim_threshold in type_k_combinations:
        print_seperator(name=agent_type.__name__)
        tulip_agent = agent_type(
            tool_library=tulip,
            top_k_functions=top_k,
            search_similarity_threshold=sim_threshold,
        )
        res = tulip_agent.query(query)
        print(f"{res=}")


if __name__ == "__main__":
    run_comparison()
