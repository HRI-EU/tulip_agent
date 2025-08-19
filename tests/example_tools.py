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


def add(a: float, b: float) -> float:
    """
    Add two numbers.

    :param a: The first number.
    :param b: The second number.
    :return: The sum of a and b.
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """
    Subtract two numbers.

    :param a: The number to be subtracted from.
    :param b: The number to subtract.
    :return: The difference of a and b.
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.

    :param a: The first number.
    :param b: The second number.
    :return: The product of a and b.
    """
    return a * b


def divide(a: float, b: float) -> float:
    """
    Divide two numbers.

    :param a: The dividend.
    :param b: The divisor.
    :return: The quotient of a and b.
    """
    return a / b


def slow(duration: int) -> str:
    """
    A function that takes some time to execute.

    :param duration: Duration the function takes to complete
    :return: Completion message
    """
    import time

    time.sleep(duration)
    return "Done"


def speak(text: str) -> str:
    """
    Loudly say something to the user via speakers.

    :param text: The text to speak.
    :return: The quotient of a and b.
    """
    return f"Successfully said `{text}`."
