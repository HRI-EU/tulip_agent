#!/usr/bin/env python3
#
#  Copyright (c) 2024-2025, Honda Research Institute Europe GmbH
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  SPDX-License-Identifier: BSD-3-Clause
#
#
"""
Tools can be created from a class' methods or from individual functions.
"""
import pprint

from tulip_agent import FunctionAnalyzer, ImportedTool


def return_hi() -> str:
    """
    Return "hi".
    """
    return "hi"


class Calculator:
    def __init__(self, divisor: float) -> None:
        self.divisor = divisor

    @staticmethod
    def add(a: float, b: float) -> float:
        """
        Add two numbers.

        :param a: The first number.
        :param b: The second number.
        :return: The sum of a and b.
        """
        return a + b


if __name__ == "__main__":
    fa = FunctionAnalyzer()

    hi_description = fa.analyze_function(return_hi)
    hi = ImportedTool(
        function_name="return_hi",
        module_name="tool_examples",
        definition=hi_description,
    )
    print(hi)
    print(hi_description)
    pprint.pprint(hi.format_for_chroma())
    print(hi.execute())

    calc = Calculator(10)
    add_description = fa.analyze_class(Calculator)[0]
    add = ImportedTool(
        function_name="add",
        module_name="tool_examples",
        definition=add_description,
        instance=calc,
    )
    print(add)
    print(add_description)
    pprint.pprint(add.format_for_chroma())
    print(add.execute(**{"a": 1, "b": 2}))
