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

from tulip_agent import DfsTulipAgent, ToolLibrary


# Set logger to INFO to show agents' internal steps
logging.basicConfig(level=logging.INFO)

tasks = [
    # "Add 2 and 5",
    # "Add the product of 3 and 4 and the product of 5 and 6",
    "Calculate the square root of the sum of the product of 3 and 4 and the product of 5 and 6",
    # "Take an image of the table and convert that to a jpg",
    # (
    #     "Calculate the area of a rectangle with length 8 units and width 5 units, "
    #     "then find the circumference of a circle with a radius equal to the square root of the rectangle's area."
    # ),
    # "Find the difference between the area of a square with side length 20 and a the area of a circle with radius 10.",
]

tulip = ToolLibrary(chroma_sub_dir="example/")
tulip.chroma_client.delete_collection("tulip")

tulip = ToolLibrary(
    chroma_sub_dir="example/",
    file_imports=[("calculator", [])],
    # file_imports=[("calculator", ["add", "subtract", "square_root"])],
    # file_imports=[("math_tools", [])],
)
agent = DfsTulipAgent(
    tool_library=tulip,
    top_k_functions=10,
    search_similarity_threshold=2,
    max_recursion_depth=2,
    max_paraphrases=1,
    max_replans=1,
    plot_task_tree=True,
)

for task in tasks:
    print(f"{task=}")
    res = agent.query(prompt=task)
    print(f"{res=}")
