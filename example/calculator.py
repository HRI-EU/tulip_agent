#!/usr/bin/env python3
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
    return x ** 0.5


def exponent(x: float, y: float):
    """
    Raises a number to the power of another.

    :param x: The base.
    :param y: The exponent.
    :return: x raised to the power of y.
    """
    return x ** y


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
