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
import math


def add(x: float, y: float):
    """
    Adds two numbers together.

    :param x: The first number to add.
    :param y: The second number to add.
    :return: The sum of x and y.
    """
    return x + y


def subtract(x: float, y: float):
    """
    Subtracts the second number from the first.

    :param x: The number to be subtracted from.
    :param y: The number to subtract.
    :return: The difference of x and y.
    """
    return x - y


def multiply(x: float, y: float):
    """
    Multiplies two numbers.

    :param x: The first number to multiply.
    :param y: The second number to multiply.
    :return: The product of x and y.
    """
    return x * y


def divide(x: float, y: float):
    """
    Divides the first number by the second.

    :param x: The numerator.
    :param y: The denominator. Must not be zero.
    :return: The quotient of x and y.
    """
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y


def square_root(x: float):
    """
    Calculates the square root of a number.

    :param x: The number to find the square root of. Must be non-negative.
    :return: The square root of x.
    """
    if x < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return x**0.5


def exponent(x: float, y: float):
    """
    Raises a number to the power of another.

    :param x: The base.
    :param y: The exponent.
    :return: x raised to the power of y.
    """
    return x**y


def modulus(x: float, y: float):
    """
    Finds the remainder when the first number is divided by the second.

    :param x: The dividend.
    :param y: The divisor.
    :return: The remainder of x divided by y.
    """
    return x % y


def sine(x: float):
    """
    Calculates the sine of an angle in radians.

    :param x: The angle in radians.
    :return: The sine of x.
    """
    return math.sin(x)


def cosine(x: float):
    """
    Calculates the cosine of an angle in radians.

    :param x: The angle in radians.
    :return: The cosine of x.
    """
    return math.cos(x)


def tangent(x: float):
    """
    Calculates the tangent of an angle in radians.

    :param x: The angle in radians.
    :return: The tangent of x.
    """
    return math.tan(x)
