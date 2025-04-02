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
"""
Example for
* setting up a tool library with tools from a file import and a class instance
* searching for tools in the tool library
"""
import logging

from calculator import TrigonometryCalculator
from tulip_agent import ToolLibrary


# Set logger to INFO to show details
logging.basicConfig(level=logging.INFO)

tasks = [
    """Add 2 and 5""",
    """Calculate the product of 2 and 5.""",
    """Calculate the square root of 8.""",
    """What is 2 + 5?""",
    """What is 2 + 4 / 3?""",
    """Draw a horse""",
    """Calculate the cosine of 90 degrees.""",
]

trigonometry_calculator = TrigonometryCalculator()

tulip = ToolLibrary(
    chroma_sub_dir="lib_example/",
    file_imports=[("calculator", [])],
    instance_imports=[trigonometry_calculator],
)

# alternatively load tools from files or class instances later on:
# tulip.load_functions_from_file(module_name="calculator")
# tulip.load_functions_from_instance(instance=trigonometry_calculator)

for task in tasks:
    print(f"{task=}")
    res = tulip.search(problem_description=task, top_k=4, similarity_threshold=1.5)
    print(f"{res=}")
