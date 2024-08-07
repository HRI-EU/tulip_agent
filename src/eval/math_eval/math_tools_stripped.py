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
import sys
from collections import Counter
from functools import reduce
from inspect import getmembers, isfunction

import numpy as np


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

    :param a: The first multiplicand.
    :param b: The second multiplicand.
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


def modulus(a: float, b: float) -> float:
    """
    Find the modulus of two numbers.

    :param a: The dividend.
    :param b: The divisor.
    :return: The remainder of the division of a by b.
    """
    return a % b


def power(base: float, exponent: float) -> float:
    """
    Raise a number to the power of another.

    :param base: The base number.
    :param exponent: The exponent.
    :return: The result of raising base to the power of exponent.
    """
    return base**exponent


def sqrt(number: float) -> float:
    """
    Calculate the square root of a number.

    :param number: The number to find the square root of.
    :return: The square root of the number.
    """
    return number**0.5


def absolute(number: float) -> float:
    """
    Find the absolute value of a number.

    :param number: The number to find the absolute value of.
    :return: The absolute value of the number.
    """
    return abs(number)


def factorial(number: int) -> int:
    """
    Calculate the factorial of a number.

    :param number: The number to find the factorial of.
    :return: The factorial of the number.
    """
    if number == 0:
        return 1
    else:
        return number * factorial(number - 1)


def gcd(a: int, b: int) -> int:
    """
    Compute the greatest common divisor of a and b.

    :param a: The first number.
    :param b: The second number.
    :return: The greatest common divisor of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """
    Compute the least common multiple of a and b.

    :param a: The first number.
    :param b: The second number.
    :return: The least common multiple of a and b.
    """
    return abs(a * b) // gcd(a, b)


def is_prime(number: int) -> bool:
    """
    Check if a number is prime.

    :param number: The number to check.
    :return: True if the number is prime, False otherwise.
    """
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True


def fibonacci_sequence(n: int) -> list:
    """
    Generate a list of Fibonacci numbers up to the nth number.

    :param n: The length of the Fibonacci sequence to generate.
    :return: A list containing the Fibonacci sequence up to the nth number.
    """
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]


def prime_factors(number: int) -> list:
    """
    Find all prime factors of a number.

    :param number: The number to find the prime factors of.
    :return: A list of the prime factors of the number.
    """
    i = 2
    factors = []
    while i * i <= number:
        if number % i:
            i += 1
        else:
            number //= i
            factors.append(i)
    if number > 1:
        factors.append(number)
    return factors


def cosine(angle: float) -> float:
    """
    Calculate the cosine of an angle in radians.

    :param angle: The angle in radians.
    :return: The cosine of the angle.
    """
    return math.cos(angle)


def sine(angle: float) -> float:
    """
    Calculate the sine of an angle in radians.

    :param angle: The angle in radians.
    :return: The sine of the angle.
    """
    return math.sin(angle)


def tangent(angle: float) -> float:
    """
    Calculate the tangent of an angle in radians.

    :param angle: The angle in radians.
    :return: The tangent of the angle.
    """
    return math.tan(angle)


def log(number: float, base: float = math.e) -> float:
    """
    Calculate the logarithm of a number with given base.

    :param number: The number to calculate the logarithm for.
    :param base: The base of the logarithm. Defaults to Euler's number.
    :return: The logarithm of the number with the given base.
    """
    return math.log(number, base)

def exp(number: float) -> float:
    """
    Calculate the exponential of a given number.

    :param number: The number to calculate the exponential for.
    :return: The exponential of the number.
    """
    return math.exp(number)


def radians_to_degrees(radians: float) -> float:
    """
    Convert radians to degrees.

    :param radians: The angle in radians.
    :return: The angle in degrees.
    """
    return math.degrees(radians)


def degrees_to_radians(degrees: float) -> float:
    """
    Convert degrees to radians.

    :param degrees: The angle in degrees.
    :return: The angle in radians.
    """
    return math.radians(degrees)


def quadratic_formula(a: float, b: float, c: float) -> tuple:
    """
    Solve a quadratic equation using the quadratic formula.

    :param a: The coefficient of x^2.
    :param b: The coefficient of x.
    :param c: The constant term.
    :return: A tuple containing the two solutions.
    """
    discriminant = math.sqrt(b**2 - 4 * a * c)
    x1 = (-b + discriminant) / (2 * a)
    x2 = (-b - discriminant) / (2 * a)
    return x1, x2


def nth_root(number: float, root: float) -> float:
    """
    Calculate the nth root of a number.

    :param number: The number to find the root of.
    :param root: The degree of the root.
    :return: The nth root of the number.
    """
    return number ** (1 / root)


def is_even(number: int) -> bool:
    """
    Check if a number is even.

    :param number: The number to check.
    :return: True if the number is even, False otherwise.
    """
    return number % 2 == 0


def is_odd(number: int) -> bool:
    """
    Check if a number is odd.

    :param number: The number to check.
    :return: True if the number is odd, False otherwise.
    """
    return number % 2 != 0

def convert_celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convert temperature from Celsius to Fahrenheit.

    :param celsius: The temperature in Celsius.
    :return: The temperature in Fahrenheit.
    """
    return (celsius * 9 / 5) + 32


def convert_fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Convert temperature from Fahrenheit to Celsius.

    :param fahrenheit: The temperature in Fahrenheit.
    :return: The temperature in Celsius.
    """
    return (fahrenheit - 32) * 5 / 9

def arithmetic_mean(numbers: list[float]) -> float:
    """
    Calculate the arithmetic mean of a list of numbers.

    :param numbers: A list of numbers.
    :return: The arithmetic mean.
    """
    return sum(x for x in numbers) / len(numbers)

def harmonic_mean(numbers: list[float]) -> float:
    """
    Calculate the harmonic mean of a list of numbers.

    :param numbers: A list of numbers.
    :return: The harmonic mean.
    """
    return len(numbers) / sum(1 / x for x in numbers)


def geometric_mean(numbers: list[float]) -> float:
    """
    Calculate the geometric mean of a list of numbers.

    :param numbers: A list of numbers.
    :return: The geometric mean.
    """
    product = math.prod(numbers)
    return product ** (1 / len(numbers))


def nth_prime(n: int) -> int:
    """
    Find the nth prime number.

    :param n: The nth position.
    :return: The nth prime number.
    """
    prime_count = 0
    num = 1
    while prime_count < n:
        num += 1
        if is_prime(num):
            prime_count += 1
    return num


def binomial_coefficient(n: int, k: int) -> int:
    """
    Calculate the binomial coefficient "n choose k".

    :param n: The number of items.
    :param k: The number of items to choose.
    :return: The binomial coefficient.
    """
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def mean_absolute_deviation(numbers: list[float]) -> float:
    """
    Calculate the mean absolute deviation of a list of numbers.

    :param numbers: A list of numbers.
    :return: The mean absolute deviation.
    """
    mean = sum(numbers) / len(numbers)
    return sum(abs(x - mean) for x in numbers) / len(numbers)


def standard_deviation(numbers: list[float]) -> float:
    """
    Calculate the standard deviation of a list of numbers.

    :param numbers: A list of numbers.
    :return: The standard deviation.
    """
    mean = sum(numbers) / len(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    return math.sqrt(variance)


def variance(numbers: list[float]) -> float:
    """
    Calculate the variance of a list of numbers.

    :param numbers: A list of numbers.
    :return: The variance.
    """
    mean = sum(numbers) / len(numbers)
    return sum((x - mean) ** 2 for x in numbers) / len(numbers)


def coefficient_of_variation(numbers: list[float]) -> float:
    """
    Calculate the coefficient of variation of a list of numbers.

    :param numbers: A list of numbers.
    :return: The coefficient of variation.
    """
    stdev = standard_deviation(numbers)
    mean = sum(numbers) / len(numbers)
    return stdev / mean


def median(numbers: list[float]) -> float:
    """
    Calculate the median of a list of numbers.

    :param numbers: A list of sorted numbers.
    :return: The median.
    """
    numbers.sort()
    n = len(numbers)
    if n % 2 == 0:
        return (numbers[n // 2 - 1] + numbers[n // 2]) / 2
    else:
        return numbers[n // 2]


def mode(numbers: list[float]) -> list:
    """
    Calculate the mode(s) of a list of numbers.

    :param numbers: A list of numbers.
    :return: A list of modes.
    """
    counts = Counter(numbers)
    max_count = max(counts.values())
    return [num for num, count in counts.items() if count == max_count]


def interquartile_range(numbers: list[float]) -> float:
    """
    Calculate the interquartile range of a list of numbers.

    :param numbers: A list of sorted numbers.
    :return: The interquartile range.
    """

    numbers.sort()
    mid_index = len(numbers) // 2
    if len(numbers) % 2 == 0:
        q1 = median(numbers[:mid_index])
        q3 = median(numbers[mid_index:])
    else:
        q1 = median(numbers[:mid_index])
        q3 = median(numbers[mid_index + 1 :])
    return q3 - q1


def range_of_numbers(numbers: list[float]) -> float:
    """
    Calculate the range of a list of numbers.

    :param numbers: A list of numbers.
    :return: The range.
    """
    return max(numbers) - min(numbers)



def is_palindrome(number: int) -> bool:
    """
    Check if a number is a palindrome.

    :param number: The number to check.
    :return: True if the number is a palindrome, False otherwise.
    """
    return str(number) == str(number)[::-1]


def sum_of_digits(number: int) -> int:
    """
    Calculate the sum of the digits of a number.

    :param number: The number.
    :return: The sum of its digits.
    """
    return sum(int(digit) for digit in str(number))


def digital_root(number: int) -> int:
    """
    Calculate the digital root of a number, which is the iterative process of summing the digits of a number,
    until a single-digit number is reached.

    :param number: The number to find the digital root of.
    :return: The digital root.
    """
    while number >= 10:
        number = sum(int(digit) for digit in str(number))
    return number



def prime_sieve(n: int) -> list:
    """
    Sieve of Eratosthenes: Find all prime numbers up to n.

    :param n: The upper limit to find primes within.
    :return: A list of prime numbers up to n.
    """
    sieve = [True] * (n + 1)
    primes = []
    for p in range(2, n + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return primes

def length_of_numbers(numbers: list[float]) -> float:
    """
    Calculate the lenght of a list of numbers.

    :param numbers: A list of numbers.
    :return: The length of the list..
    """
    return len(numbers)

def product_of_numbers(numbers: list[float]) -> float:
    """
    Calculate the product of all numbers in a list.

    :param numbers: A list of numbers.
    :return: The product of all numbers.
    """
    return reduce((lambda x, y: x * y), numbers)

def sum_of_numbers(numbers: list[float]) -> float:
    """
    Calculate the sum of all numbers in a list.

    :param numbers: A list of numbers.
    :return: The sum of all numbers.
    """
    return reduce((lambda x, y: x + y), numbers)

def number_of_divisors(n: int) -> int:
    """
    Calculate the number of divisors of a number.

    :param n: The number.
    :return: The number of divisors of n.
    """
    divisors = 0
    for i in range(1, n + 1):
        if n % i == 0:
            divisors += 1
    return divisors

def is_divisible_by(a: int, b: int) -> bool:
    """
    Calculate if a is divisible by b.

    :param a: The number to divide.
    :param b: The number to test.
    :return: True if a is divisible by b, False otherwise.
    """
    return a % b == 0

def round(number: float, decimals: int) -> float:
    """
    Returns the evenly round to the given decimals.

    :param number: The number to round.
    :param decimals: The precision to round to.
    :return: The rounded number.
    """
    return np.round(number, decimals=decimals)

def floor(number: float) -> float:
    """
    Return the floor of the number.

    :param number: The number.
    :return: The floor of the number.
    """
    return np.floor(number)

def ceil(number: float) -> float:
    """
    Return the ceiling of the number.

    :param number: The number.
    :return: The ceiling of the number.
    """
    return np.ceil(number)

if __name__ == "__main__":
    current_module = sys.modules[__name__]
    print(current_module)
    functions = [
        (n, f)
        for n, f in getmembers(current_module, isfunction)
        if f.__module__ == "__main__"
    ]
    print(f"Number of functions: {len(functions)}")
    print(f"Functions: {functions}")
    print(f"Number of duplicate functions: {len(functions) - len(set(functions))}")

    from tulip_agent.function_analyzer import FunctionAnalyzer

    fa = FunctionAnalyzer()
    for name, function in functions:
        print(name)
        description = fa.analyze_function(function)
        print(description)
