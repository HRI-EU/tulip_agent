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
mte: math_tools_extended
"""


# algebra


def add_numbers(a: float, b: float) -> float:
    """
    Calculate the sum of two numbers.

    :param a: The first number to be added.
    :param b: The second number to be added.
    :return: The sum of a and b.
    """
    return a + b


def subtract_numbers(a: float, b: float) -> float:
    """
    Calculate the difference between two numbers.

    :param a: The minuend.
    :param b: The subtrahend.
    :return: The difference between a and b.
    """
    return a - b


def multiply_numbers(a: float, b: float) -> float:
    """
    Calculate the product of two numbers.

    :param a: The first factor.
    :param b: The second factor.
    :return: The product of a and b.
    """
    return a * b


def divide_numbers(a: float, b: float) -> float:
    """
    Calculate the quotient of two numbers.

    :param a: The dividend.
    :param b: The divisor.
    :return: The quotient of a divided by b.
    :raises ValueError: If b is 0.
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


def solve_quadratic_equation(a: float, b: float, c: float) -> tuple:
    """
    Solve a quadratic equation of the form ax^2 + bx + c = 0.

    :param a: The coefficient of x^2.
    :param b: The coefficient of x.
    :param c: The constant term.
    :return: A tuple containing the two solutions.
    :raises ValueError: If the equation does not have real solutions.
    """
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        raise ValueError("The equation does not have real solutions.")
    x1 = (-b + discriminant**0.5) / (2 * a)
    x2 = (-b - discriminant**0.5) / (2 * a)
    return x1, x2


def calculate_determinant(matrix: list[list[float]]) -> float:
    """
    Calculate the determinant of a 2x2 matrix.

    :param matrix: A 2x2 matrix represented as a list of lists containing floats.
    :return: The determinant of the matrix.
    """
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def find_slope(point1: tuple[float, ...], point2: tuple[float, ...]) -> float:
    """
    Find the slope of a line given two points.

    :param point1: A tuple representing the first point (x1, y1).
    :param point2: A tuple representing the second point (x2, y2).
    :return: The slope of the line.
    """
    return (point2[1] - point1[1]) / (point2[0] - point1[0])


def calculate_area_of_triangle(base: float, height: float) -> float:
    """
    Calculate the area of a triangle given the base and height.

    :param base: The base of the triangle.
    :param height: The height of the triangle.
    :return: The area of the triangle.
    """
    return 0.5 * base * height


def calculate_mean(values: list[float]) -> float:
    """
    Calculate the mean of a list of numbers.

    :param values: A list of floats representing the numbers.
    :return: The mean of the numbers.
    """
    return sum(values) / len(values)


def find_root_linear_equation(a: float, b: float) -> float:
    """
    Find the root of a linear equation in the form ax + b = 0.

    :param a: The coefficient of x.
    :param b: The constant term.
    :return: The root of the equation.
    """
    return -b / a


def calculate_area_of_rectangle(length: float, width: float) -> float:
    """
    Calculate the area of a rectangle.

    This function takes the length and width of a rectangle and returns the area.
    The area is calculated by multiplying the length by the width.

    :param length: The length of the rectangle.
    :param width: The width of the rectangle.
    :return: The area of the rectangle.
    """
    return length * width


def calculate_volume_of_cylinder(radius: float, height: float) -> float:
    """
    Calculate the volume of a cylinder.

    This function computes the volume of a cylinder given its radius and height.
    The formula used is V = πr^2h, where r is the radius and h is the height.

    :param radius: The radius of the cylinder.
    :param height: The height of the cylinder.
    :return: The volume of the cylinder.
    """
    import math

    return math.pi * radius**2 * height


def calculate_perimeter_of_square(side_length: float) -> float:
    """
    Calculate the perimeter of a square.

    This function returns the perimeter of a square, which is calculated
    as four times the length of one side.

    :param side_length: The length of one side of the square.
    :return: The perimeter of the square.
    """
    return 4 * side_length


def calculate_simple_interest(principal: float, rate: float, time: float) -> float:
    """
    Calculate simple interest.

    This function calculates the simple interest earned/paid over a period of time.
    The formula used is I = PRT, where P is the principal amount, R is the annual interest rate,
    and T is the time in years.

    :param principal: The principal amount.
    :param rate: The annual interest rate (as a decimal).
    :param time: The time in years.
    :return: The simple interest.
    """
    return principal * rate * time


def calculate_compound_interest(
    principal: float, rate: float, times_compounded: int, years: float
) -> float:
    """
    Calculate compound interest.

    This function calculates the compound interest using the formula
    A = P(1 + r/n)^(nt), where P is the principal amount, r is the annual interest rate,
    n is the number of times the interest is compounded per year, and t is the time in years.

    :param principal: The principal amount.
    :param rate: The annual interest rate (as a decimal).
    :param times_compounded: The number of times interest is compounded per year.
    :param years: The time in years.
    :return: The amount of money accumulated after n years, including interest.
    """
    return principal * (1 + rate / times_compounded) ** (times_compounded * years)


def calculate_area_of_circle(radius: float) -> float:
    """
    Calculate the area of a circle given its radius.

    :param radius: The radius of the circle.
    :return: The area of the circle.
    """
    import math

    return math.pi * radius**2


def calculate_circumference_of_circle(radius: float) -> float:
    """
    Calculate the circumference of a circle given its radius.

    :param radius: The radius of the circle.
    :return: The circumference of the circle.
    """
    import math

    return 2 * math.pi * radius


def calculate_area_of_square(side_length: float) -> float:
    """
    Calculate the area of a square given the length of its side.

    :param side_length: The length of the side of the square.
    :return: The area of the square.
    """
    return side_length**2


def calculate_volume_of_cube(side_length: float) -> float:
    """
    Calculate the volume of a cube given the length of its side.

    :param side_length: The length of the side of the cube.
    :return: The volume of the cube.
    """
    return side_length**3


def calculate_pythagorean_theorem(a: float, b: float) -> float:
    """
    Calculate the length of the hypotenuse of a right-angled triangle given the lengths of the other two sides.

    :param a: The length of one side of the triangle.
    :param b: The length of the other side of the triangle.
    :return: The length of the hypotenuse of the triangle.
    """
    import math

    return math.sqrt(a**2 + b**2)


def calculate_factorial(n: int) -> int:
    """
    Calculate the factorial of a given number.

    The factorial of a non-negative integer n is the product of all positive integers less than or equal to n.
    It is denoted by n!.

    :param n: The non-negative integer to calculate the factorial of.
    :return: The factorial of n.
    """
    if n == 0:
        return 1
    return n * calculate_factorial(n - 1)


def calculate_gcd(a: int, b: int) -> int:
    """
    Calculate the greatest common divisor (GCD) of two numbers.

    The GCD of two integers is the largest positive integer that divides each of the integers without a remainder.

    :param a: First integer.
    :param b: Second integer.
    :return: The greatest common divisor of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def calculate_lcm(a: int, b: int) -> int:
    """
    Calculate the least common multiple (LCM) of two numbers.

    The LCM of two integers is the smallest positive integer that is divisible by both a and b.

    :param a: First integer.
    :param b: Second integer.
    :return: The least common multiple of a and b.
    """
    return abs(a * b) // calculate_gcd(a, b)


def calculate_exponential(base: float, exponent: int) -> float:
    """
    Calculate the exponential of a base raised to a given exponent.

    This function computes base raised to the power of exponent.

    :param base: The base value.
    :param exponent: The exponent value.
    :return: The result of base raised to the power of exponent.
    """
    return base**exponent


def calculate_logarithm(base: float, value: float) -> float:
    """
    Calculate the logarithm of a value to a given base.

    The logarithm of a number is the exponent to which another fixed number, the base,
    must be raised to produce that number.

    :param base: The base of the logarithm.
    :param value: The value to calculate the logarithm for.
    :return: The logarithm of value to the given base.
    """
    import math

    return math.log(value, base)


def calculate_median(numbers: list[float]) -> float:
    """
    Calculate the median of a list of numbers.

    The function sorts the list of numbers and finds the median, which is the middle value
    in an ordered list of values. If the list has an even number of elements, the median is
    the average of the two middle numbers.

    :param numbers: A list of numbers for which the median is to be calculated.
    :return: The median of the list of numbers.
    """
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    else:
        return sorted_numbers[mid]


def calculate_standard_deviation(numbers: list[float]) -> float:
    """
    Calculate the standard deviation of a list of numbers.

    Standard deviation is a measure of the amount of variation or dispersion of a set of values.
    A low standard deviation indicates that the values tend to be close to the mean of the set,
    while a high standard deviation indicates that the values are spread out over a wider range.

    :param numbers: A list of numbers for which the standard deviation is to be calculated.
    :return: The standard deviation of the list of numbers.
    """
    mean = sum(numbers) / len(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    return variance**0.5


def calculate_mode(numbers: list[float]) -> list:
    """
    Calculate the mode(s) of a list of numbers.

    The mode is the value that appears most frequently in a data set. A data set may have one mode,
    more than one mode, or no mode at all.

    :param numbers: A list of numbers for which the mode(s) is to be calculated.
    :return: A list containing the mode(s) of the list of numbers.
    """
    frequency = {}
    for number in numbers:
        frequency[number] = frequency.get(number, 0) + 1
    max_frequency = max(frequency.values())
    modes = [key for key, val in frequency.items() if val == max_frequency]
    return modes


def calculate_range(numbers: list[float]) -> float:
    """
    Calculate the range of a list of numbers.

    The range is the difference between the highest and lowest values in a set of numbers.

    :param numbers: A list of numbers for which the range is to be calculated.
    :return: The range of the list of numbers.
    """
    return max(numbers) - min(numbers)


def calculate_sum_of_squares(numbers: list[float]) -> float:
    """
    Calculate the sum of the squares of a list of numbers.

    This function takes each number in the list, squares it, and then sums up all the squared numbers.

    :param numbers: A list of numbers for which the sum of squares is to be calculated.
    :return: The sum of the squares of the list of numbers.
    """
    return sum(x**2 for x in numbers)


def calculate_volume_of_sphere(radius: float) -> float:
    """
    Calculate the volume of a sphere given its radius.

    :param radius: The radius of the sphere.
    :return: The volume of the sphere.
    """
    from math import pi

    return (4 / 3) * pi * radius**3


def calculate_surface_area_of_sphere(radius: float) -> float:
    """
    Calculate the surface area of a sphere given its radius.

    :param radius: The radius of the sphere.
    :return: The surface area of the sphere.
    """
    from math import pi

    return 4 * pi * radius**2


def calculate_volume_of_cone(radius: float, height: float) -> float:
    """
    Calculate the volume of a cone given its radius and height.

    :param radius: The radius of the base of the cone.
    :param height: The height of the cone.
    :return: The volume of the cone.
    """
    from math import pi

    return (1 / 3) * pi * radius**2 * height


def calculate_surface_area_of_cylinder(radius: float, height: float) -> float:
    """
    Calculate the surface area of a cylinder given its radius and height.

    :param radius: The radius of the base of the cylinder.
    :param height: The height of the cylinder.
    :return: The surface area of the cylinder.
    """
    from math import pi

    return 2 * pi * radius * (radius + height)


def calculate_volume_of_pyramid(
    base_length: float, base_width: float, height: float
) -> float:
    """
    Calculate the volume of a pyramid given its base length, base width, and height.

    :param base_length: The length of the base of the pyramid.
    :param base_width: The width of the base of the pyramid.
    :param height: The height of the pyramid.
    :return: The volume of the pyramid.
    """
    return (1 / 3) * base_length * base_width * height


def calculate_variance(numbers: list[float]) -> float:
    """
    Calculate the variance of a list of numbers.

    :param numbers: A list of numbers for which the variance is to be calculated
    :return: The variance of the numbers
    """
    mean = sum(numbers) / len(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    return variance


def calculate_cubic_root(number: float) -> float:
    """
    Calculate the cubic root of a given number.

    :param number: The number to calculate the cubic root for
    :return: The cubic root of the number
    """
    return number ** (1 / 3)


def calculate_percent_difference(value1: float, value2: float) -> float:
    """
    Calculate the percent difference between two values.

    :param value1: The first value
    :param value2: The second value
    :return: The percent difference between the two values
    """
    difference = abs(value1 - value2)
    average = (value1 + value2) / 2
    percent_difference = (difference / average) * 100
    return percent_difference


def calculate_slope_intercept_form(x1: float, y1: float, x2: float, y2: float) -> tuple:
    """
    Calculate the slope and y-intercept of the line through two points.

    :param x1: The x-coordinate of the first point
    :param y1: The y-coordinate of the first point
    :param x2: The x-coordinate of the second point
    :param y2: The y-coordinate of the second point
    :return: A tuple containing the slope and y-intercept of the line
    """
    slope = (y2 - y1) / (x2 - x1)
    y_intercept = y1 - slope * x1
    return slope, y_intercept


def calculate_arithmetic_progression_sum(n: int, a1: float, an: float) -> float:
    """
    Calculate the sum of the first n terms of an arithmetic progression.

    :param n: The number of terms
    :param a1: The first term of the progression
    :param an: The nth term of the progression
    :return: The sum of the first n terms of the arithmetic progression
    """
    return (n / 2) * (a1 + an)


def calculate_quartic_root(number: float) -> float:
    """
    Calculate the quartic (fourth) root of a given number.

    :param number: The number to find the quartic root of.
    :return: The quartic root of the number.
    """
    return number**0.25


def calculate_harmonic_mean(numbers: list[float]) -> float:
    """
    Calculate the harmonic mean of a list of numbers.

    :param numbers: A list of numbers to calculate the harmonic mean of.
    :return: The harmonic mean of the numbers.
    """
    n = len(numbers)
    denominator = sum(1 / x for x in numbers)
    return n / denominator


def calculate_geometric_mean(numbers: list[float]) -> float:
    """
    Calculate the geometric mean of a list of numbers.

    :param numbers: A list of numbers to calculate the geometric mean of.
    :return: The geometric mean of the numbers.
    """
    product = 1
    n = len(numbers)
    for number in numbers:
        product *= number
    return product ** (1 / n)


def calculate_coterminal_angle(angle: float) -> float:
    """
    Calculate a coterminal angle in degrees for a given angle.

    :param angle: The original angle in degrees.
    :return: A positive coterminal angle of the given angle within the range 0 to 360 degrees.
    """
    return angle % 360


def calculate_inverse_sine(value: float) -> float:
    """
    Calculate the inverse sine (arcsin) of a value.

    :param value: The value to calculate the arcsin for, which must be in the range [-1, 1].
    :return: The arcsin of the value in radians.
    """
    import math

    return math.asin(value)


def calculate_linear_interpolation(
    x0: float, y0: float, x1: float, y1: float, x: float
) -> float:
    """
    Calculate the linear interpolation of a value.

    Given two points (x0, y0) and (x1, y1) on a line, and the x value for which
    the y value needs to be interpolated, this function calculates the corresponding
    y value using the formula of linear interpolation.

    :param x0: The x-coordinate of the first point.
    :param y0: The y-coordinate of the first point.
    :param x1: The x-coordinate of the second point.
    :param y1: The y-coordinate of the second point.
    :param x: The x-coordinate for which the y-coordinate is to be interpolated.
    :return: The interpolated y-coordinate.
    """
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def calculate_cramer_rule(
    a1: float, b1: float, c1: float, a2: float, b2: float, c2: float
) -> tuple:
    """
    Solve a system of linear equations using Cramer's Rule.

    Given a system of two linear equations in the form:
    a1*x + b1*y = c1
    a2*x + b2*y = c2
    this function solves for x and y using Cramer's Rule.

    :param a1: Coefficient of x in the first equation.
    :param b1: Coefficient of y in the first equation.
    :param c1: Constant term of the first equation.
    :param a2: Coefficient of x in the second equation.
    :param b2: Coefficient of y in the second equation.
    :param c2: Constant term of the second equation.
    :return: A tuple (x, y) representing the solution.
    """
    d = a1 * b2 - a2 * b1
    dx = c1 * b2 - c2 * b1
    dy = a1 * c2 - a2 * c1
    if d == 0:
        raise ValueError("No solution or infinite solutions.")
    else:
        return dx / d, dy / d


def calculate_binomial_coefficient(n: int, k: int) -> int:
    """
    Calculate the binomial coefficient, also known as "n choose k".

    The binomial coefficient is the number of ways to choose k items from n items
    without regard to order. It is used in various probability and statistics calculations.

    :param n: The total number of items.
    :param k: The number of items to choose.
    :return: The binomial coefficient.
    """
    from math import factorial

    return factorial(n) // (factorial(k) * factorial(n - k))


def calculate_nth_term_of_arithmetic_sequence(a: int, d: int, n: int) -> int:
    """
    Calculate the nth term of an arithmetic sequence.

    Given the first term (a), the common difference (d), and the term position (n),
    this function calculates the value of the nth term in the arithmetic sequence.

    :param a: The first term of the arithmetic sequence.
    :param d: The common difference between terms.
    :param n: The position of the term to calculate.
    :return: The nth term of the arithmetic sequence.
    """
    return a + (n - 1) * d


def calculate_diagonal_of_rectangle(length: float, width: float) -> float:
    """
    Calculate the length of the diagonal of a rectangle.

    Given the length and width of a rectangle, this function calculates the length
    of the diagonal using the Pythagorean theorem.

    :param length: The length of the rectangle.
    :param width: The width of the rectangle.
    :return: The length of the diagonal.
    """
    return (length**2 + width**2) ** 0.5


def calculate_quadratic_formula(a: float, b: float, c: float) -> tuple:
    """
    Calculate the roots of a quadratic equation ax^2 + bx + c = 0.
    The function uses the quadratic formula to find the roots. It handles complex roots as well.

    :param a: Coefficient of x^2
    :param b: Coefficient of x
    :param c: Constant term
    :return: A tuple containing the two roots of the quadratic equation.
    """
    import cmath

    discriminant = cmath.sqrt(b**2 - 4 * a * c)
    root1 = (-b + discriminant) / (2 * a)
    root2 = (-b - discriminant) / (2 * a)
    return root1, root2


def calculate_midpoint(x1: float, y1: float, x2: float, y2: float) -> tuple:
    """
    Calculate the midpoint of a line segment defined by two points (x1, y1) and (x2, y2).
    The midpoint is calculated using the formula ((x1 + x2) / 2, (y1 + y2) / 2).

    :param x1: x-coordinate of the first point
    :param y1: y-coordinate of the first point
    :param x2: x-coordinate of the second point
    :param y2: y-coordinate of the second point
    :return: A tuple representing the midpoint (x, y) of the line segment.
    """
    return (x1 + x2) / 2, (y1 + y2) / 2


def calculate_direct_variation_constant(x: float, y: float) -> float:
    """
    Calculate the constant of variation k in a direct variation y = kx.
    In a direct variation, y varies directly as x, and the ratio y/x is constant.

    :param x: The independent variable value
    :param y: The dependent variable value
    :return: The constant of variation k.
    """
    return y / x


def calculate_inverse_variation_constant(x: float, y: float) -> float:
    """
    Calculate the constant of variation k in an inverse variation xy = k.
    In an inverse variation, y varies inversely as x, and the product xy is constant.

    :param x: The independent variable value
    :param y: The dependent variable value
    :return: The constant of variation k.
    """
    return x * y


def calculate_point_slope_form(x1: float, y1: float, slope: float, x: float) -> float:
    """
    Calculate the y-coordinate of a point on a line, given its slope and a point on the line.
    The function uses the point-slope form of a line equation: y - y1 = m(x - x1), where m is the slope.

    :param x1: x-coordinate of the known point on the line
    :param y1: y-coordinate of the known point on the line
    :param slope: The slope of the line
    :param x: x-coordinate of the point whose y-coordinate is to be calculated
    :return: The y-coordinate of the point on the line.
    """
    return slope * (x - x1) + y1


def calculate_subtraction_of_matrices(
    matrix_a: list[list[float]], matrix_b: list[list[float]]
) -> list[list[float]]:
    """
    Calculate the subtraction of two matrices.
    The function assumes both matrices have the same dimensions.

    :param matrix_a: A list of lists where each inner list represents a row in the first matrix.
    :param matrix_b: A list of lists where each inner list represents a row in the second matrix.
    :return: A new matrix (list of lists) representing the subtraction of matrix_a and matrix_b.
    """
    return [
        [matrix_a[i][j] - matrix_b[i][j] for j in range(len(matrix_a[0]))]
        for i in range(len(matrix_a))
    ]


def calculate_dot_product(vector_a: list[float], vector_b: list[float]) -> float:
    """
    Calculate the dot product of two vectors.
    The function assumes both vectors have the same number of elements.

    :param vector_a: A list of numbers representing the first vector.
    :param vector_b: A list of numbers representing the second vector.
    :return: A single float value representing the dot product of the two vectors.
    """
    return sum(a * b for a, b in zip(vector_a, vector_b))


def calculate_matrix_transpose(matrix: list[list[float]]) -> list[list[float]]:
    """
    Calculate the transpose of a matrix.

    :param matrix: A list of lists where each inner list represents a row in the matrix.
    :return: A new matrix (list of lists) representing the transpose of the original matrix.
    """
    return list(map(list, zip(*matrix)))


def calculate_determinant_of_2x2_matrix(matrix: list[list[float]]) -> float:
    """
    Calculate the determinant of a 2x2 matrix.
    The function assumes the matrix is 2x2.

    :param matrix: A list of lists where each inner list represents a row in the 2x2 matrix.
    :return: A single float value representing the determinant of the matrix.
    """
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def calculate_scalar_multiplication_of_matrix(
    scalar: float, matrix: list[list[float]]
) -> list[list[float]]:
    """
    Calculate the scalar multiplication of a matrix.
    The function works for matrices of any dimension.

    :param scalar: A float value representing the scalar to multiply with the matrix.
    :param matrix: A list of lists where each inner list represents a row in the matrix.
    :return: A new matrix (list of lists) representing the result of scalar multiplication.
    """
    return [[scalar * element for element in row] for row in matrix]


def calculate_polynomial_value(coefficients: list[float], x: float) -> float:
    """
    Calculate the value of a polynomial for a given x.
    The polynomial is defined as coefficients[0]*x^n + coefficients[1]*x^(n-1) + ... + coefficients[n].

    :param coefficients: A list of coefficients from the highest degree to the constant term.
    :param x: The value of the variable x.
    :return: The polynomial value.
    """
    return sum(coef * x**i for i, coef in enumerate(reversed(coefficients)))


def calculate_euclidean_distance(
    point1: tuple[float, ...], point2: tuple[float, ...]
) -> float:
    """
    Calculate the Euclidean distance between two points in n-dimensional space.
    The distance is calculated using the formula sqrt(sum((p1_i - p2_i)^2 for i in dimensions)).

    :param point1: A tuple representing the coordinates of the first point.
    :param point2: A tuple representing the coordinates of the second point.
    :return: The Euclidean distance between the two points.
    """
    return sum((a - b) ** 2 for a, b in zip(point1, point2)) ** 0.5


def calculate_system_of_linear_equations(
    matrix: list[list[float]], constants: list[float]
) -> list:
    """
    Solve a system of linear equations represented in matrix form.
    This function uses the numpy library to solve the system of equations.

    :param matrix: A 2D list where each sublist represents the coefficients of variables in one equation.
    :param constants: A list of constants for each equation.
    :return: A list of variable values that solve the system of equations.
    """
    import numpy as np

    return list(np.linalg.solve(np.array(matrix), np.array(constants)))


def calculate_derivative_at_point(function, x: float, h: float = 1e-5) -> float:
    """
    Calculate the derivative of a function at a given point using the limit definition.
    The derivative is calculated as (f(x+h) - f(x)) / h.

    :param function: The function for which the derivative is calculated.
    :param x: The point at which the derivative is calculated.
    :param h: A small step size to approximate the derivative, default is 1e-5.
    :return: The derivative of the function at point x.
    """
    return (function(x + h) - function(x)) / h


def calculate_inverse_matrix(matrix: list[list[float]]) -> list:
    """
    Calculate the inverse of a square matrix.
    This function uses the numpy library to calculate the inverse of the matrix.

    :param matrix: A 2D list representing a square matrix.
    :return: The inverse of the matrix.
    """
    import numpy as np

    return np.linalg.inv(np.array(matrix)).tolist()


def calculate_sum_of_geometric_series(a: float, r: float, n: int) -> float:
    """
    Calculate the sum of the first n terms of a geometric series.

    :param a: The first term of the geometric series.
    :param r: The common ratio of the geometric series.
    :param n: The number of terms to sum up.
    :return: The sum of the first n terms of the geometric series.
    """
    return a * (1 - r**n) / (1 - r)


def calculate_sum_of_infinite_geometric_series(a: float, r: float) -> float:
    """
    Calculate the sum of an infinite geometric series.

    :param a: The first term of the geometric series.
    :param r: The common ratio of the geometric series.
    :return: The sum of the infinite geometric series if |r| < 1, else returns float('inf').
    """
    if abs(r) < 1:
        return a / (1 - r)
    else:
        return float("inf")


def calculate_cubic_equation_root(a: float, b: float, c: float, d: float) -> float:
    """
    Calculate one real root of a cubic equation of the form ax^3 + bx^2 + cx + d = 0.

    :param a: Coefficient of x^3.
    :param b: Coefficient of x^2.
    :param c: Coefficient of x.
    :param d: Constant term.
    :return: One real root of the cubic equation.
    """
    f = ((3 * c / a) - (b**2 / a**2)) / 3
    g = ((2 * b**3 / a**3) - (9 * b * c / a**2) + (27 * d / a)) / 27
    h = (g**2 / 4) + (f**3 / 27)

    if h > 0:
        R = -(g / 2) + (h**0.5)
        S = R ** (1 / 3)
        T = -(g / 2) - (h**0.5)
        U = abs(T) ** (1 / 3) * (1 if T < 0 else -1)
        root = (S + U) - (b / (3 * a))
    else:
        root = -1  # Placeholder for more complex cases

    return root


def calculate_nth_term_of_geometric_sequence(a: float, r: float, n: int) -> float:
    """
    Calculate the nth term of a geometric sequence.

    :param a: The first term of the geometric sequence.
    :param r: The common ratio of the geometric sequence.
    :param n: The term number to find.
    :return: The nth term of the geometric sequence.
    """
    return a * r ** (n - 1)


def calculate_sum_of_n_natural_numbers(n: int) -> int:
    """
    Calculate the sum of the first n natural numbers.

    :param n: The number of terms to sum up.
    :return: The sum of the first n natural numbers.
    """
    return n * (n + 1) // 2


def calculate_hypotenuse(leg_a: float, leg_b: float) -> float:
    """
    Calculate the length of the hypotenuse of a right-angled triangle.

    :param leg_a: Length of the first leg of the triangle.
    :param leg_b: Length of the second leg of the triangle.
    :return: Length of the hypotenuse.
    """
    return (leg_a**2 + leg_b**2) ** 0.5


def calculate_cosine_law_side(a: float, b: float, c: float) -> float:
    """
    Calculate the length of a side of a triangle using the cosine law.

    :param a: Length of the first side of the triangle.
    :param b: Length of the second side of the triangle.
    :param c: Angle opposite the side to be calculated, in degrees.
    :return: Length of the third side.
    """
    from math import cos, radians

    return (a**2 + b**2 - 2 * a * b * cos(radians(c))) ** 0.5


def calculate_cosine_law_angle(a: float, b: float, c: float) -> float:
    """
    Calculate an angle of a triangle using the cosine law.

    :param a: Length of the first side of the triangle.
    :param b: Length of the second side of the triangle.
    :param c: Length of the side opposite the angle to be calculated.
    :return: Angle opposite the side c, in degrees.
    """
    from math import acos, degrees

    return degrees(acos((a**2 + b**2 - c**2) / (2 * a * b)))


def calculate_sine_law_side(a: float, A: float, B: float) -> float:
    """
    Calculate the length of a side of a triangle using the sine law.

    :param a: Length of a known side of the triangle.
    :param A: Angle opposite the known side, in degrees.
    :param B: Angle opposite the side to be calculated, in degrees.
    :return: Length of the side opposite angle B.
    """
    from math import radians, sin

    return a * sin(radians(B)) / sin(radians(A))


def calculate_sine_law_angle(a: float, A: float, b: float) -> float:
    """
    Calculate an angle of a triangle using the sine law.

    :param a: Length of a known side of the triangle.
    :param A: Angle opposite the known side, in degrees.
    :param b: Length of the side opposite the angle to be calculated.
    :return: Angle opposite the side b, in degrees.
    """
    from math import asin, degrees, radians, sin

    return degrees(asin(b * sin(radians(A)) / a))


def calculate_linear_equation_slope_intercept(
    x1: float, y1: float, x2: float, y2: float
) -> tuple:
    """
    Calculate the slope and y-intercept of a linear equation given two points.

    :param x1: The x-coordinate of the first point.
    :param y1: The y-coordinate of the first point.
    :param x2: The x-coordinate of the second point.
    :param y2: The y-coordinate of the second point.
    :return: A tuple containing the slope and y-intercept of the linear equation.
    """
    slope = (y2 - y1) / (x2 - x1)
    y_intercept = y1 - slope * x1
    return slope, y_intercept


def calculate_perimeter_of_rectangle(length: float, width: float) -> float:
    """
    Calculate the perimeter of a rectangle.

    :param length: The length of the rectangle.
    :param width: The width of the rectangle.
    :return: The perimeter of the rectangle.
    """
    return 2 * (length + width)


def calculate_volume_of_prism(base_area: float, height: float) -> float:
    """
    Calculate the volume of a prism.

    :param base_area: The area of the base of the prism.
    :param height: The height of the prism.
    :return: The volume of the prism.
    """
    return base_area * height


def calculate_angle_sum_of_polygon(n_sides: int) -> float:
    """
    Calculate the sum of the interior angles of a polygon.

    :param n_sides: The number of sides of the polygon.
    :return: The sum of the interior angles of the polygon in degrees.
    """
    return (n_sides - 2) * 180


def calculate_area_of_parallelogram(base: float, height: float) -> float:
    """
    Calculate the area of a parallelogram.

    :param base: The length of the base of the parallelogram.
    :param height: The height of the parallelogram.
    :return: The area of the parallelogram.
    """
    return base * height


def calculate_sum_of_cubes(n: int) -> int:
    """
    Calculate the sum of the cubes of the first n natural numbers.

    :param n: The number of terms in the series.
    :return: The sum of the cubes of the first n natural numbers.
    """
    return sum(i**3 for i in range(1, n + 1))


def calculate_double_angle_cosine(cos_x: float) -> float:
    """
    Calculate the cosine of a double angle given the cosine of the original angle.

    :param cos_x: The cosine of the original angle x.
    :return: The cosine of the double angle 2x.
    """
    return 2 * cos_x**2 - 1


def calculate_pascals_triangle_row(n: int) -> list:
    """
    Calculate the nth row of Pascal's triangle.

    :param n: The row number to calculate, where n=0 is the first row.
    :return: A list representing the nth row of Pascal's triangle.
    """
    row = [1]
    for k in range(1, n + 1):
        row.append(row[k - 1] * (n - k + 1) // k)
    return row


def calculate_fibonacci_number(n: int) -> int:
    """
    Calculate the nth Fibonacci number.

    :param n: The position of the Fibonacci number to calculate.
    :return: The nth Fibonacci number.
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def calculate_annuity_payment(principal: float, rate: float, periods: int) -> float:
    """
    Calculate the annuity payment for a loan based on constant payments and a constant interest rate.

    :param principal: The total amount of the loan.
    :param rate: The interest rate per period.
    :param periods: The number of periods over which the loan is amortized.
    :return: The annuity payment amount.
    """
    return principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)


def calculate_sum_of_odd_numbers(n: int) -> int:
    """
    Calculate the sum of the first n odd numbers.

    :param n: The number of odd numbers to sum up.
    :return: The sum of the first n odd numbers.
    """
    return n**2


def calculate_sum_of_even_numbers(n: int) -> int:
    """
    Calculate the sum of the first n even numbers.

    :param n: The number of even numbers to sum up.
    :return: The sum of the first n even numbers.
    """
    return n * (n + 1)


def calculate_product_of_n_numbers(args: list[int]) -> int:
    """
    Calculate the product of n given numbers.

    :param args: A list with a variable number of integers to be multiplied.
    :return: The product of the given numbers.
    """
    product = 1
    for num in args:
        product *= num
    return product


def calculate_nth_root(value: float, n: int) -> float:
    """
    Calculate the nth root of a given value.

    :param value: The value to find the nth root of.
    :param n: The degree of the root.
    :return: The nth root of the value.
    """
    return value ** (1 / n)


def calculate_sum_of_arithmetic_series(n: int, a1: float, an: float) -> float:
    """
    Calculate the sum of an arithmetic series.

    :param n: The number of terms in the series.
    :param a1: The first term of the series.
    :param an: The last term of the series.
    :return: The sum of the arithmetic series.
    """
    return (n * (a1 + an)) / 2


def calculate_surface_area_of_cone(radius: float, slant_height: float) -> float:
    """
    Calculate the surface area of a cone.

    :param radius: The radius of the base of the cone.
    :param slant_height: The slant height of the cone.
    :return: The surface area of the cone.
    """
    import math

    return math.pi * radius * (radius + slant_height)


def calculate_volume_of_rectangular_prism(
    length: float, width: float, height: float
) -> float:
    """
    Calculate the volume of a rectangular prism.

    :param length: The length of the rectangular prism.
    :param width: The width of the rectangular prism.
    :param height: The height of the rectangular prism.
    :return: The volume of the rectangular prism.
    """
    return length * width * height


def calculate_perimeter_of_triangle(side1: float, side2: float, side3: float) -> float:
    """
    Calculate the perimeter of a triangle.

    :param side1: The length of the first side of the triangle.
    :param side2: The length of the second side of the triangle.
    :param side3: The length of the third side of the triangle.
    :return: The perimeter of the triangle.
    """
    return side1 + side2 + side3


def calculate_area_of_rhombus(diagonal1: float, diagonal2: float) -> float:
    """
    Calculate the area of a rhombus.

    :param diagonal1: The length of the first diagonal of the rhombus.
    :param diagonal2: The length of the second diagonal of the rhombus.
    :return: The area of the rhombus.
    """
    return (diagonal1 * diagonal2) / 2


def calculate_volume_of_tetrahedron(edge_length: float) -> float:
    """
    Calculate the volume of a regular tetrahedron.

    :param edge_length: The length of an edge of the tetrahedron.
    :return: The volume of the tetrahedron.
    """
    import math

    return (edge_length**3) / (6 * math.sqrt(2))


def calculate_sum_of_powers(n: int, power: int) -> int:
    """
    Calculate the sum of the powers of all natural numbers up to n.

    :param n: The upper limit of the natural numbers to be considered.
    :param power: The power to which each natural number is raised.
    :return: The sum of the powers of all natural numbers up to n.
    """
    return sum([i**power for i in range(1, n + 1)])


def calculate_perimeter_of_hexagon(side_length: float) -> float:
    """
    Calculate the perimeter of a hexagon given the length of one side.

    :param side_length: The length of one side of the hexagon.
    :return: The perimeter of the hexagon.
    """
    return 6 * side_length


def calculate_volume_of_torus(major_radius: float, minor_radius: float) -> float:
    """
    Calculate the volume of a torus given its major and minor radii.

    :param major_radius: The major radius of the torus (distance from the tube's center to the center of the torus).
    :param minor_radius: The minor radius of the torus (radius of the tube).
    :return: The volume of the torus.
    """
    import math

    return 2 * math.pi**2 * major_radius * minor_radius**2


def calculate_cofactor(matrix: list[list[float]], row: int, col: int) -> float:
    """
    Calculate the cofactor of a matrix element specified by its row and column indices.

    :param matrix: The matrix as a list of lists.
    :param row: The row index of the element (0-based).
    :param col: The column index of the element (0-based).
    :return: The cofactor of the specified element.
    """

    def minor(m: list[list[float]], i: int, j: int) -> list[list[float]]:
        return [r[:j] + r[j + 1 :] for r in (m[:i] + m[i + 1 :])]

    def determinant(m: list[list[float]]) -> float:
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]
        det = 0
        for c in range(len(m)):
            det += ((-1) ** c) * m[0][c] * determinant(minor(m, 0, c))
        return det

    return ((-1) ** (row + col)) * determinant(minor(matrix, row, col))


def calculate_perimeter_of_octagon(side_length: float) -> float:
    """
    Calculate the perimeter of an octagon.

    :param side_length: The length of one side of the octagon.
    :return: The perimeter of the octagon.
    """
    return 8 * side_length


def calculate_area_of_ellipse(major_axis: float, minor_axis: float) -> float:
    """
    Calculate the area of an ellipse.

    :param major_axis: The length of the major axis of the ellipse.
    :param minor_axis: The length of the minor axis of the ellipse.
    :return: The area of the ellipse.
    """
    import math

    return math.pi * major_axis * minor_axis


def calculate_sum_of_natural_numbers(n: int) -> int:
    """
    Calculate the sum of the first n natural numbers.

    :param n: The number of terms.
    :return: The sum of the first n natural numbers.
    """
    return n * (n + 1) // 2


def calculate_volume_of_ellipsoid(a: float, b: float, c: float) -> float:
    """
    Calculate the volume of an ellipsoid.

    :param a: The semi-axis length along the x-axis.
    :param b: The semi-axis length along the y-axis.
    :param c: The semi-axis length along the z-axis.
    :return: The volume of the ellipsoid.
    """
    import math

    return 4 / 3 * math.pi * a * b * c


def calculate_linear_function_value(m: float, x: float, b: float) -> float:
    """
    Calculate the value of a linear function.

    :param m: The slope of the line.
    :param x: The x-coordinate for which to calculate the y-value.
    :param b: The y-intercept of the line.
    :return: The y-value of the linear function.
    """
    return m * x + b


def calculate_prime_factors(n: int) -> list:
    """
    Calculate all prime factors of a given number.

    :param n: The number to find the prime factors for.
    :return: A list of prime factors of n.
    """
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def calculate_least_common_multiple(a: int, b: int) -> int:
    """
    Calculate the Least Common Multiple (LCM) of two numbers.

    :param a: The first number.
    :param b: The second number.
    :return: The LCM of a and b.
    """

    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    return abs(a * b) // gcd(a, b)


def calculate_cubic_equation_discriminant(a: int, b: int, c: int, d: int) -> int:
    """
    Calculate the discriminant of a cubic equation ax^3 + bx^2 + cx + d = 0.

    :param a: Coefficient of x^3.
    :param b: Coefficient of x^2.
    :param c: Coefficient of x.
    :param d: Constant term.
    :return: The discriminant of the cubic equation.
    """
    discriminant = (
        18 * a * b * c * d
        - 4 * b**3 * d
        + b**2 * c**2
        - 4 * a * c**3
        - 27 * a**2 * d**2
    )
    return discriminant


def calculate_perfect_numbers(limit: int) -> list:
    """
    Calculate all perfect numbers up to a given limit.

    :param limit: The upper limit to search for perfect numbers.
    :return: A list of all perfect numbers up to the limit.
    """

    def is_perfect(n):
        return sum(i for i in range(1, n) if n % i == 0) == n

    return [n for n in range(1, limit) if is_perfect(n)]


def calculate_sum_of_n_fibonacci_numbers(n: int) -> int:
    """
    Calculate the sum of the first n Fibonacci numbers.

    :param n: The number of terms in the Fibonacci sequence to sum up.
    :return: The sum of the first n Fibonacci numbers.
    """
    a, b = 0, 1
    sum_fib = 0
    for _ in range(n):
        sum_fib += b
        a, b = b, a + b
    return sum_fib


def calculate_trapezoid_area(base1: float, base2: float, height: float) -> float:
    """
    Calculate the area of a trapezoid given its bases and height.

    :param base1: The length of the first base of the trapezoid.
    :param base2: The length of the second base of the trapezoid.
    :param height: The height of the trapezoid.
    :return: The area of the trapezoid.
    """
    return (base1 + base2) * height / 2


def calculate_regular_polygon_perimeter(side_length: float, num_sides: int) -> float:
    """
    Calculate the perimeter of a regular polygon.

    :param side_length: The length of one side of the polygon.
    :param num_sides: The total number of sides in the polygon.
    :return: The perimeter of the regular polygon.
    """
    return side_length * num_sides


def calculate_cylinder_surface_area(radius: float, height: float) -> float:
    """
    Calculate the surface area of a cylinder.

    :param radius: The radius of the cylinder's base.
    :param height: The height of the cylinder.
    :return: The surface area of the cylinder.
    """
    from math import pi

    return 2 * pi * radius * (radius + height)


def calculate_logarithmic_expression(base: float, value: float) -> float:
    """
    Calculate the logarithm of a value with a specified base.

    :param base: The base of the logarithm.
    :param value: The value to compute the logarithm for.
    :return: The logarithm of the value with the specified base.
    """
    import math

    return math.log(value, base)


def calculate_sum_of_n_primes(n: int) -> int:
    """
    Calculate the sum of the first n prime numbers.

    :param n: The number of prime numbers to sum up.
    :return: The sum of the first n prime numbers.
    """
    sum_, count, num = 0, 0, 2
    while count < n:
        if is_prime(num):
            sum_ += num
            count += 1
        num += 1
    return sum_


def calculate_sum_of_n_primes_squared(n: int) -> int:
    """
    Calculate the sum of the squares of the first n prime numbers.

    :param n: The number of prime numbers to consider.
    :return: The sum of the squares of the first n prime numbers.
    """
    sum_, count, num = 0, 0, 2
    while count < n:
        if is_prime(num):
            sum_ += num**2
            count += 1
        num += 1
    return sum_


def calculate_product_of_n_primes(n: int) -> int:
    """
    Calculate the product of the first n prime numbers.

    :param n: The number of prime numbers to multiply.
    :return: The product of the first n prime numbers.
    """
    product, count, num = 1, 0, 2
    while count < n:
        if is_prime(num):
            product *= num
            count += 1
        num += 1
    return product


def calculate_nth_prime(n: int) -> int:
    """
    Find the nth prime number.

    :param n: The position of the prime number to find.
    :return: The nth prime number.
    """
    count, num = 0, 2
    while True:
        if is_prime(num):
            count += 1
            if count == n:
                return num
        num += 1


def calculate_sum_of_prime_factors(number: int) -> int:
    """
    Calculate the sum of all prime factors of a given number.

    :param number: The number to find the prime factors of.
    :return: The sum of all prime factors of the number.
    """
    sum, factor = 0, 2
    while factor <= number:
        while number % factor == 0 and is_prime(factor):
            sum += factor
            number /= factor
        factor += 1
    return sum


def calculate_sum_of_n_squared_numbers(n: int) -> int:
    """
    Calculate the sum of the first n squared numbers.

    :param n: The number of terms in the sequence.
    :return: The sum of the first n squared numbers.
    """
    return sum(i**2 for i in range(1, n + 1))


def calculate_sum_of_n_inverse_numbers(n: int) -> float:
    """
    Calculate the sum of the inverses of the first n natural numbers.

    :param n: The number of terms in the sequence.
    :return: The sum of the inverses of the first n natural numbers.
    """
    return sum(1 / i for i in range(1, n + 1))


def calculate_linear_equation_y(mx: float, c: float) -> float:
    """
    Calculate the y value of a linear equation given the slope (m) and y-intercept (c).

    :param mx: The value of the slope times x (mx).
    :param c: The y-intercept of the linear equation.
    :return: The y value of the linear equation.
    """
    return mx + c


def calculate_perimeter_of_pentagon(side_length: float) -> float:
    """
    Calculate the perimeter of a pentagon given the length of a side.

    :param side_length: The length of a side of the pentagon.
    :return: The perimeter of the pentagon.
    """
    return 5 * side_length


def calculate_volume_of_hexahedron(edge_length: float) -> float:
    """
    Calculate the volume of a hexahedron (cube) given the length of an edge.

    :param edge_length: The length of an edge of the hexahedron.
    :return: The volume of the hexahedron.
    """
    return edge_length**3


# analysis


def calculate_surface_area_of_parallelepiped(
    length: float, width: float, height: float
) -> float:
    """
    Calculate the surface area of a parallelepiped.

    :param length: The length of the parallelepiped.
    :param width: The width of the parallelepiped.
    :param height: The height of the parallelepiped.
    :return: The surface area of the parallelepiped.
    """
    return 2 * (length * width + width * height + height * length)


def calculate_volume_of_parallelepiped(
    length: float, width: float, height: float
) -> float:
    """
    Calculate the volume of a parallelepiped.

    :param length: The length of the parallelepiped.
    :param width: The width of the parallelepiped.
    :param height: The height of the parallelepiped.
    :return: The volume of the parallelepiped.
    """
    return length * width * height


def calculate_regular_polygon_area(num_sides: int, side_length: float) -> float:
    """
    Calculate the area of a regular polygon.

    :param num_sides: The number of sides of the polygon.
    :param side_length: The length of each side of the polygon.
    :return: The area of the regular polygon.
    """
    from math import pi, tan

    return (num_sides * side_length**2) / (4 * tan(pi / num_sides))


def calculate_spherical_cap_volume(radius: float, height: float) -> float:
    """
    Calculate the volume of a spherical cap.

    :param radius: The radius of the sphere.
    :param height: The height of the cap.
    :return: The volume of the spherical cap.
    """
    from math import pi

    return (1 / 3) * pi * height**2 * (3 * radius - height)


def calculate_elliptic_integral_of_second_kind(
    phi: float, eccentricity: float
) -> float:
    """
    Calculate the elliptic integral of the second kind.

    :param phi: The amplitude of the elliptic integral.
    :param eccentricity: The eccentricity of the elliptic integral.
    :return: The value of the elliptic integral of the second kind.
    """
    from math import sin, sqrt

    from scipy.integrate import quad

    def integrand(theta):
        return sqrt(1 - eccentricity**2 * sin(theta) ** 2)

    return quad(integrand, 0, phi)[0]


def calculate_surface_area_of_tetrahedron(edge_length: float) -> float:
    """
    Calculate the surface area of a regular tetrahedron.

    :param edge_length: The length of an edge of the tetrahedron.
    :return: The surface area of the tetrahedron.
    """
    return (edge_length**2) * (3**0.5)


def calculate_volume_of_octahedron(edge_length: float) -> float:
    """
    Calculate the volume of a regular octahedron.

    :param edge_length: The length of an edge of the octahedron.
    :return: The volume of the octahedron.
    """
    return (2**0.5 / 3) * edge_length**3


def calculate_centroid_of_triangle(
    x1: float, y1: float, x2: float, y2: float, x3: float, y3: float
) -> tuple:
    """
    Calculate the centroid of a triangle given its vertices.

    :param x1: The x-coordinate of the first vertex.
    :param y1: The y-coordinate of the first vertex.
    :param x2: The x-coordinate of the second vertex.
    :param y2: The y-coordinate of the second vertex.
    :param x3: The x-coordinate of the third vertex.
    :param y3: The y-coordinate of the third vertex.
    :return: A tuple containing the x and y coordinates of the centroid.
    """
    return (x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3


def calculate_moment_of_inertia_of_rectangle(width: float, height: float) -> float:
    """
    Calculate the moment of inertia of a rectangle about its centroidal axis.

    :param width: The width of the rectangle.
    :param height: The height of the rectangle.
    :return: The moment of inertia of the rectangle.
    """
    return (width * height**3) / 12


def calculate_angular_velocity(frequency: float) -> float:
    """
    Calculate the angular velocity given the frequency.

    :param frequency: The frequency in cycles per second (Hz).
    :return: The angular velocity in radians per second.
    """
    from math import pi

    return 2 * pi * frequency


def calculate_secant(angle: float) -> float:
    """
    Calculate the secant of an angle given in radians.

    :param angle: The angle in radians for which to calculate the secant.
    :return: The secant of the given angle.
    """
    import math

    return 1 / math.cos(angle)


def calculate_cosecant(angle: float) -> float:
    """
    Calculate the cosecant of an angle given in radians.

    :param angle: The angle in radians for which to calculate the cosecant.
    :return: The cosecant of the given angle.
    """
    import math

    return 1 / math.sin(angle)


def calculate_arc_length(radius: float, angle: float) -> float:
    """
    Calculate the arc length of a circle segment based on the radius and central angle.

    :param radius: The radius of the circle.
    :param angle: The central angle of the circle segment in radians.
    :return: The length of the arc.
    """
    return radius * angle


def calculate_tangent_line_equation(slope: float, point: tuple[float, ...]) -> str:
    """
    Calculate the equation of a tangent line given its slope and a point it passes through.

    :param slope: The slope of the tangent line.
    :param point: A tuple (x, y) representing a point through which the tangent line passes.
    :return: The equation of the tangent line in the format 'y = mx + b'.
    """
    x, y = point
    b = y - slope * x
    return f"y = {slope}x + {b}"


def calculate_area_of_sector(radius: float, angle: float) -> float:
    """
    Calculate the area of a sector of a circle based on its radius and central angle.

    :param radius: The radius of the circle.
    :param angle: The central angle of the sector in radians.
    :return: The area of the sector.
    """
    return 0.5 * radius**2 * angle


def calculate_surface_area_of_prism(
    length: float, width: float, height: float
) -> float:
    """
    Calculate the surface area of a rectangular prism.

    :param length: The length of the prism
    :param width: The width of the prism
    :param height: The height of the prism
    :return: The surface area of the rectangular prism
    """
    return 2 * (length * width + width * height + height * length)


def calculate_volume_of_regular_pyramid(base_area: float, height: float) -> float:
    """
    Calculate the volume of a regular pyramid.

    :param base_area: The area of the pyramid's base
    :param height: The height of the pyramid from the base to the apex
    :return: The volume of the pyramid
    """
    return (1 / 3) * base_area * height


def calculate_circumradius_of_triangle(
    side_a: float, side_b: float, side_c: float
) -> float:
    """
    Calculate the circumradius of a triangle.

    :param side_a: Length of side a of the triangle
    :param side_b: Length of side b of the triangle
    :param side_c: Length of side c of the triangle
    :return: The circumradius of the triangle
    """
    s = (side_a + side_b + side_c) / 2  # semi-perimeter
    area = (s * (s - side_a) * (s - side_b) * (s - side_c)) ** 0.5
    return (side_a * side_b * side_c) / (4 * area)


def calculate_inradius_of_triangle(
    side_a: float, side_b: float, side_c: float
) -> float:
    """
    Calculate the inradius of a triangle.

    :param side_a: Length of side a of the triangle
    :param side_b: Length of side b of the triangle
    :param side_c: Length of side c of the triangle
    :return: The inradius of the triangle
    """
    s = (side_a + side_b + side_c) / 2  # semi-perimeter
    area = (s * (s - side_a) * (s - side_b) * (s - side_c)) ** 0.5
    return area / s


def calculate_torus_volume(major_radius: float, minor_radius: float) -> float:
    """
    Calculate the volume of a torus.

    :param major_radius: The major radius of the torus (distance from the tube's center to the center of the torus)
    :param minor_radius: The minor radius of the torus (radius of the tube)
    :return: The volume of the torus
    """
    import math

    return 2 * math.pi**2 * major_radius * minor_radius**2


def calculate_trigonometric_sum(angle: float, n: int) -> float:
    """
    Calculate the sum of trigonometric series up to n terms for a given angle.

    :param angle: The angle in radians for which the trigonometric sum is calculated.
    :param n: The number of terms up to which the sum is calculated.
    :return: The sum of the trigonometric series up to n terms.
    """
    import math

    sum_series = 0
    for i in range(1, n + 1):
        sum_series += math.sin(i * angle) + math.cos(i * angle)
    return sum_series


def calculate_surface_area_of_pyramid(base_length: float, slant_height: float) -> float:
    """
    Calculate the surface area of a pyramid.

    :param base_length: The length of the base of the pyramid.
    :param slant_height: The slant height of the pyramid.
    :return: The surface area of the pyramid.
    """
    base_area = base_length**2
    perimeter = 4 * base_length
    lateral_area = 0.5 * perimeter * slant_height
    return base_area + lateral_area


def calculate_logarithmic_derivative(expression: str, variable: str) -> str:
    """
    Calculate the derivative of a logarithmic expression with respect to a given variable.

    :param expression: The logarithmic expression as a string.
    :param variable: The variable with respect to which the derivative is calculated.
    :return: The derivative of the logarithmic expression as a string.
    """
    from sympy import diff, log, symbols

    x = symbols(variable)
    expr = log(eval(expression))
    derivative = diff(expr, x)
    return str(derivative)


def calculate_circular_segment_area(radius: float, angle: float) -> float:
    """
    Calculate the area of a circular segment given its radius and central angle.

    :param radius: The radius of the circle.
    :param angle: The central angle of the segment in radians.
    :return: The area of the circular segment.
    """
    import math

    return (radius**2 / 2) * (angle - math.sin(angle))


def calculate_spherical_volume(radius: float) -> float:
    """
    Calculate the volume of a sphere given its radius.

    :param radius: The radius of the sphere.
    :return: The volume of the sphere.
    """
    from math import pi

    return (4 / 3) * pi * radius**3


def calculate_surface_area_of_torus(major_radius: float, minor_radius: float) -> float:
    """
    Calculate the surface area of a torus given its major and minor radii.

    :param major_radius: The major radius of the torus (distance from the tube's center to the center of the torus).
    :param minor_radius: The minor radius of the torus (radius of the tube).
    :return: The surface area of the torus.
    """
    from math import pi

    return 4 * pi**2 * major_radius * minor_radius


def calculate_catenary_length(a: float, x1: float, x2: float) -> float:
    """
    Calculate the length of a catenary curve between two points.

    :param a: The catenary constant, which determines the steepness of the curve.
    :param x1: The x-coordinate of the starting point.
    :param x2: The x-coordinate of the ending point.
    :return: The length of the catenary curve between the two points.
    """
    from math import sinh

    return a * (sinh(x2 / a) - sinh(x1 / a))


def calculate_golden_ratio_approximation(n: int) -> float:
    """
    Calculate an approximation of the golden ratio using Fibonacci sequence.

    :param n: The number of terms in the Fibonacci sequence to use for the approximation.
    :return: An approximation of the golden ratio.
    """

    def fibonacci(num):
        a, b = 0, 1
        for _ in range(num):
            a, b = b, a + b
        return a

    return fibonacci(n + 1) / fibonacci(n)


def calculate_weight_on_planet(mass: float, gravity: float) -> float:
    """
    Calculate the weight of an object on a planet given its mass and the planet's gravity.

    :param mass: Mass of the object in kilograms.
    :param gravity: Gravity of the planet in m/s^2.
    :return: Weight of the object on the planet in Newtons.
    """
    return mass * gravity


def calculate_perimeter_of_rhomboid(base: float, height: float) -> float:
    """
    Calculate the perimeter of a rhomboid given its base and height.

    :param base: Length of the base of the rhomboid in units.
    :param height: Height of the rhomboid in units.
    :return: Perimeter of the rhomboid in the same units as base and height.
    """
    return 2 * (base + height)


def calculate_relative_velocity(v1: float, v2: float) -> float:
    """
    Calculate the relative velocity between two objects.

    :param v1: Velocity of the first object in m/s.
    :param v2: Velocity of the second object in m/s.
    :return: Relative velocity between the two objects in m/s.
    """
    return v1 - v2


def calculate_simple_harmonic_motion_amplitude(
    period: float, velocity_max: float
) -> float:
    """
    Calculate the amplitude of simple harmonic motion given the period and maximum velocity.

    :param period: Period of the motion in seconds.
    :param velocity_max: Maximum velocity during the motion in m/s.
    :return: Amplitude of the motion in meters.
    """
    from math import pi

    return velocity_max / (2 * pi / period)


def calculate_time_of_flight(velocity: float, angle: float) -> float:
    """
    Calculate the time of flight of a projectile given its initial velocity and launch angle.

    :param velocity: Initial velocity of the projectile in m/s.
    :param angle: Launch angle of the projectile in degrees.
    :return: Time of flight of the projectile in seconds.
    """
    from math import radians, sin

    g = 9.81  # Acceleration due to gravity in m/s^2
    return (2 * velocity * sin(radians(angle))) / g


def calculate_surface_area_of_hexagonal_prism(
    side_length: float, height: float
) -> float:
    """
    Calculate the surface area of a hexagonal prism.

    :param side_length: The length of one side of the hexagonal base.
    :param height: The height of the prism.
    :return: The surface area of the hexagonal prism.
    """
    base_area = 3 * (3**0.5) / 2 * side_length**2
    side_area = 6 * side_length * height
    return 2 * base_area + side_area


def calculate_volume_of_hexagonal_prism(side_length: float, height: float) -> float:
    """
    Calculate the volume of a hexagonal prism.

    :param side_length: The length of one side of the hexagonal base.
    :param height: The height of the prism.
    :return: The volume of the hexagonal prism.
    """
    base_area = 3 * (3**0.5) / 2 * side_length**2
    return base_area * height


def calculate_conical_frustum_volume(
    top_radius: float, bottom_radius: float, height: float
) -> float:
    """
    Calculate the volume of a conical frustum.

    :param top_radius: The radius of the top circle of the frustum.
    :param bottom_radius: The radius of the bottom circle of the frustum.
    :param height: The height of the frustum.
    :return: The volume of the conical frustum.
    """
    from math import pi

    return (
        1
        / 3
        * pi
        * height
        * (bottom_radius**2 + bottom_radius * top_radius + top_radius**2)
    )


def calculate_triple_product(
    v1: list[float], v2: list[float], v3: list[float]
) -> float:
    """
    Calculate the scalar triple product of three vectors.

    :param v1: A list of three elements representing the first vector.
    :param v2: A list of three elements representing the second vector.
    :param v3: A list of three elements representing the third vector.
    :return: The scalar triple product as a float.
    """
    return (
        v1[0] * (v2[1] * v3[2] - v2[2] * v3[1])
        - v1[1] * (v2[0] * v3[2] - v2[2] * v3[0])
        + v1[2] * (v2[0] * v3[1] - v2[1] * v3[0])
    )


def calculate_vector_cross_product(v1: list[float], v2: list[float]) -> list[float]:
    """
    Calculate the cross product of two vectors.

    :param v1: A list of three elements representing the first vector.
    :param v2: A list of three elements representing the second vector.
    :return: A list representing the cross product vector.
    """
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    ]


def calculate_vector_projection(v1: list[float], v2: list[float]) -> list:
    """
    Calculate the projection of vector v1 onto vector v2.

    :param v1: A list of elements representing the first vector.
    :param v2: A list of elements representing the second vector.
    :return: A list representing the projection vector of v1 onto v2.
    """
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v2_squared = sum(a * a for a in v2)
    return [dot_product / magnitude_v2_squared * a for a in v2]


def calculate_vector_angle(v1: list[float], v2: list[float]) -> float:
    """
    Calculate the angle in radians between two vectors.

    :param v1: A list of elements representing the first vector.
    :param v2: A list of elements representing the second vector.
    :return: The angle in radians between the two vectors as a float.
    """
    from math import acos, sqrt

    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = sqrt(sum(a * a for a in v1))
    magnitude_v2 = sqrt(sum(a * a for a in v2))
    return acos(dot_product / (magnitude_v1 * magnitude_v2))


def calculate_vector_unit(v: list[float]) -> list:
    """
    Calculate the unit vector of a given vector.

    :param v: A list of elements representing the vector.
    :return: A list representing the unit vector.
    """
    from math import sqrt

    magnitude_v = sqrt(sum(a * a for a in v))
    return [a / magnitude_v for a in v]


def calculate_surface_area_of_octahedron(edge_length: float) -> float:
    """
    Calculate the surface area of an octahedron.

    :param edge_length: The length of an edge of the octahedron.
    :return: The surface area of the octahedron.
    """
    return 2 * (3**0.5) * edge_length**2


def calculate_spherical_sector_volume(radius: float, height: float) -> float:
    """
    Calculate the volume of a spherical sector.

    :param radius: The radius of the sphere.
    :param height: The height of the spherical cap.
    :return: The volume of the spherical sector.
    """
    from math import pi

    return (1 / 3) * pi * height**2 * (3 * radius - height)


def calculate_spherical_zone_volume(outer_radius: float, inner_radius: float) -> float:
    """
    Calculate the volume of a spherical zone.

    :param outer_radius: The outer radius of the spherical zone.
    :param inner_radius: The inner radius of the spherical zone.
    :return: The volume of the spherical zone.
    """
    from math import pi

    return (4 / 3) * pi * (outer_radius**3 - inner_radius**3)


def calculate_surface_area_of_regular_tetrahedron(edge_length: float) -> float:
    """
    Calculate the surface area of a regular tetrahedron.

    :param edge_length: The length of an edge of the tetrahedron.
    :return: The surface area of the tetrahedron.
    """
    return (edge_length**2) * (3**0.5)


def calculate_paraboloid_volume(radius: float, height: float) -> float:
    """
    Calculate the volume of a paraboloid.

    :param radius: The radius of the base of the paraboloid.
    :param height: The height of the paraboloid.
    :return: The volume of the paraboloid.
    """
    from math import pi

    return (1 / 2) * pi * (radius**2) * height


def calculate_surface_area_of_cuboid(
    length: float, width: float, height: float
) -> float:
    """
    Calculate the surface area of a cuboid.

    :param length: The length of the cuboid.
    :param width: The width of the cuboid.
    :param height: The height of the cuboid.
    :return: The surface area of the cuboid.
    """
    return 2 * (length * width + width * height + height * length)


def calculate_volume_of_trapezoidal_prism(
    base1: float, base2: float, height: float, length: float
) -> float:
    """
    Calculate the volume of a trapezoidal prism.

    :param base1: The length of the first base of the trapezoidal cross-section.
    :param base2: The length of the second base of the trapezoidal cross-section.
    :param height: The height of the trapezoidal cross-section.
    :param length: The length of the prism.
    :return: The volume of the trapezoidal prism.
    """
    return ((base1 + base2) / 2) * height * length


def calculate_regular_polygon_interior_angle(sides: int) -> float:
    """
    Calculate the measure of each interior angle of a regular polygon.

    :param sides: The number of sides of the polygon.
    :return: The measure of an interior angle in degrees.
    """
    return (sides - 2) * 180 / sides


def calculate_circular_ring_area(outer_radius: float, inner_radius: float) -> float:
    """
    Calculate the area of a circular ring.

    :param outer_radius: The radius of the outer circle.
    :param inner_radius: The radius of the inner circle.
    :return: The area of the circular ring.
    """
    from math import pi

    return pi * (outer_radius**2 - inner_radius**2)


def calculate_sine_wave_value(
    amplitude: float, frequency: float, phase: float, time: float
) -> float:
    """
    Calculate the value of a sine wave at a given time.

    :param amplitude: The amplitude of the sine wave.
    :param frequency: The frequency of the sine wave.
    :param phase: The phase shift of the sine wave.
    :param time: The time at which to evaluate the sine wave.
    :return: The value of the sine wave at the given time.
    """
    from math import pi, sin

    return amplitude * sin(2 * pi * frequency * time + phase)


def calculate_sum_of_odd_numbers_up_to_n(n: int) -> int:
    """
    Calculate the sum of all odd numbers up to a given number n.

    :param n: The upper limit number up to which the sum of odd numbers is calculated.
    :return: The sum of all odd numbers up to n.
    """
    return sum(number for number in range(1, n + 1, 2))


def calculate_cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """
    Calculate the cosine similarity between two vectors.

    :param vector_a: A list of floats representing the first vector.
    :param vector_b: A list of floats representing the second vector.
    :return: The cosine similarity between vector_a and vector_b.
    """
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = sum(a**2 for a in vector_a) ** 0.5
    magnitude_b = sum(b**2 for b in vector_b) ** 0.5
    return dot_product / (magnitude_a * magnitude_b)


def calculate_permutation(n: int, r: int) -> int:
    """
    Calculate the number of permutations of n items taken r at a time.

    :param n: The total number of items.
    :param r: The number of items to take at a time.
    :return: The number of permutations.
    """
    from math import factorial

    return factorial(n) // factorial(n - r)


def calculate_trapezoidal_rule(f, a: float, b: float, n: int) -> float:
    """
    Calculate the definite integral of a function using the trapezoidal rule.

    :param f: The function to integrate.
    :param a: The lower limit of integration.
    :param b: The upper limit of integration.
    :param n: The number of trapezoids.
    :return: The approximate value of the definite integral.
    """
    h = (b - a) / n
    return (h / 2) * (f(a) + 2 * sum(f(a + i * h) for i in range(1, n)) + f(b))


def calculate_harmonic_series(n: int) -> float:
    """
    Calculate the sum of the first n terms of the harmonic series.

    :param n: The number of terms in the harmonic series to sum.
    :return: The sum of the first n terms of the harmonic series.
    """
    return sum(1 / i for i in range(1, n + 1))


def calculate_sum_of_quadratic_series(a: int, n: int) -> int:
    """
    Calculate the sum of the first n terms of a quadratic series of the form an^2.

    :param a: The coefficient of n^2 in the quadratic series.
    :param n: The number of terms to sum up in the series.
    :return: The sum of the first n terms of the quadratic series.
    """
    return a * n * (n + 1) * (2 * n + 1) // 6


def calculate_surface_area_of_spherical_cap(radius: float, height: float) -> float:
    """
    Calculate the surface area of a spherical cap.

    :param radius: The radius of the sphere from which the cap is a part.
    :param height: The height of the cap.
    :return: The surface area of the spherical cap.
    """
    from math import pi

    return 2 * pi * radius * height


def calculate_volume_of_frustum(
    top_radius: float, bottom_radius: float, height: float
) -> float:
    """
    Calculate the volume of a frustum of a right circular cone.

    :param top_radius: The radius of the smaller circular top face of the frustum.
    :param bottom_radius: The radius of the larger circular bottom face of the frustum.
    :param height: The height of the frustum.
    :return: The volume of the frustum.
    """
    from math import pi

    return (
        (1 / 3)
        * pi
        * height
        * (bottom_radius**2 + bottom_radius * top_radius + top_radius**2)
    )


def calculate_hyperbolic_cosine(x: float) -> float:
    """
    Calculate the hyperbolic cosine of x.

    :param x: The value to calculate the hyperbolic cosine for.
    :return: The hyperbolic cosine of x.
    """
    return (2.718281828459045**x + 2.718281828459045 ** (-x)) / 2


def calculate_sum_of_square_roots(n: int) -> float:
    """
    Calculate the sum of the square roots of the first n natural numbers.

    :param n: The number of terms in the sequence to sum.
    :return: The sum of the square roots of the first n natural numbers.
    """
    return sum([i**0.5 for i in range(1, n + 1)])


def calculate_log_sum_exp(values: list[float]) -> float:
    """
    Calculate the log-sum-exp of a list of values, a numerically stable way to compute the logarithm
    of the sum of exponentials of input elements.

    :param values: A list of values.
    :return: The log-sum-exp of the input values.
    """
    import math

    max_val = max(values)
    exps = [math.exp(val - max_val) for val in values]
    return max_val + math.log(sum(exps))


def calculate_simpsons_rule(f, a: float, b: float, n: int) -> float:
    """
    Approximate the definite integral of f(x) from a to b by Simpson's rule.

    :param f: The function to integrate.
    :param a: The lower limit of integration.
    :param b: The upper limit of integration.
    :param n: The number of intervals (must be even).
    :return: The approximate definite integral of f(x) from a to b.
    """
    h = (b - a) / n
    x = [a + i * h for i in range(n + 1)]
    fx = [f(xi) for xi in x]
    return (h / 3) * (
        fx[0]
        + fx[-1]
        + 4 * sum(fx[i] for i in range(1, n, 2))
        + 2 * sum(fx[i] for i in range(2, n - 1, 2))
    )


def calculate_cubic_polynomial_roots(a: float, b: float, c: float, d: float) -> list:
    """
    Calculate the roots of a cubic polynomial ax^3 + bx^2 + cx + d = 0.

    :param a: Coefficient of x^3.
    :param b: Coefficient of x^2.
    :param c: Coefficient of x.
    :param d: Constant term.
    :return: A list containing the roots of the cubic polynomial.
    """
    import numpy as np

    coefficients = [a, b, c, d]
    roots = np.roots(coefficients)
    return roots.tolist()


def calculate_euler_mascheroni_constant(n: int) -> float:
    """
    Approximate the Euler-Mascheroni constant using the first n terms of the series.

    :param n: The number of terms to use in the approximation.
    :return: The approximate value of the Euler-Mascheroni constant.
    """
    import math

    return sum([1 / i for i in range(1, n + 1)]) - math.log(n)


def calculate_surface_area_of_spherical_wedge(radius: float, height: float) -> float:
    """
    Calculate the surface area of a spherical wedge.

    :param radius: The radius of the sphere from which the spherical wedge is a part.
    :param height: The height of the spherical wedge.
    :return: The surface area of the spherical wedge.
    """
    from math import pi

    return 2 * pi * radius * height


def calculate_volume_of_spherical_wedge(radius: float, angle: float) -> float:
    """
    Calculate the volume of a spherical wedge.

    :param radius: The radius of the sphere from which the spherical wedge is a part.
    :param angle: The angle at the tip of the spherical wedge in radians.
    :return: The volume of the spherical wedge.
    """
    from math import pi

    return (2 / 3) * pi * radius**3 * angle / (2 * pi)


def calculate_circular_cylinder_volume(radius: float, height: float) -> float:
    """
    Calculate the volume of a circular cylinder.

    :param radius: The radius of the base of the cylinder.
    :param height: The height of the cylinder.
    :return: The volume of the circular cylinder.
    """
    from math import pi

    return pi * radius**2 * height


def calculate_regular_dodecahedron_volume(edge_length: float) -> float:
    """
    Calculate the volume of a regular dodecahedron.

    :param edge_length: The length of an edge of the dodecahedron.
    :return: The volume of the regular dodecahedron.
    """
    from math import sqrt

    return (15 + 7 * sqrt(5)) / 4 * edge_length**3


def calculate_regular_icosahedron_volume(edge_length: float) -> float:
    """
    Calculate the volume of a regular icosahedron.

    :param edge_length: The length of an edge of the icosahedron.
    :return: The volume of the regular icosahedron.
    """
    from math import sqrt

    return (5 * (3 + sqrt(5)) / 12) * edge_length**3


def calculate_sum_of_n_cube_numbers(n: int) -> int:
    """
    Calculate the sum of the first n cube numbers.
    The formula used is: S_n = (n(n + 1) / 2)^2

    :param n: The number of terms in the sequence
    :return: The sum of the first n cube numbers
    """
    return (n * (n + 1) // 2) ** 2


def calculate_trapezoidal_area(a: float, b: float, h: float) -> float:
    """
    Calculate the area of a trapezoid.
    The formula used is: A = ((a + b) / 2) * h

    :param a: The length of the first parallel side
    :param b: The length of the second parallel side
    :param h: The height of the trapezoid, perpendicular to the parallel sides
    :return: The area of the trapezoid
    """
    return ((a + b) / 2) * h


def calculate_regular_tetrahedron_volume(a: float) -> float:
    """
    Calculate the volume of a regular tetrahedron.
    The formula used is: V = (a^3) / (6 * sqrt(2))

    :param a: The length of an edge of the tetrahedron
    :return: The volume of the tetrahedron
    """
    return (a**3) / (6 * (2**0.5))


def calculate_circular_segment_height(r: float, chord_length: float) -> float:
    """
    Calculate the height of a circular segment based on the radius and chord length.
    The formula used is: h = r - sqrt(r^2 - (chord_length / 2)^2)

    :param r: The radius of the circle
    :param chord_length: The length of the chord defining the segment
    :return: The height of the circular segment
    """
    return r - (r**2 - (chord_length / 2) ** 2) ** 0.5


def calculate_sum_of_natural_numbers_upto_n(n: int) -> int:
    """
    Calculate the sum of all natural numbers up to and including n.

    :param n: The upper limit of the natural numbers to sum.
    :return: The sum of all natural numbers up to and including n.
    """
    return n * (n + 1) // 2


def calculate_area_of_trapezium(base1: float, base2: float, height: float) -> float:
    """
    Calculate the area of a trapezium using its bases and height.

    :param base1: The length of the first base of the trapezium.
    :param base2: The length of the second base of the trapezium.
    :param height: The height of the trapezium.
    :return: The area of the trapezium.
    """
    return 0.5 * (base1 + base2) * height


def calculate_circumference_of_ellipse(
    semi_major_axis: float, semi_minor_axis: float
) -> float:
    """
    Calculate the circumference of an ellipse using its semi-major and semi-minor axes.

    :param semi_major_axis: The length of the semi-major axis of the ellipse.
    :param semi_minor_axis: The length of the semi-minor axis of the ellipse.
    :return: An approximation of the circumference of the ellipse.
    """
    import math

    h = ((semi_major_axis - semi_minor_axis) ** 2) / (
        (semi_major_axis + semi_minor_axis) ** 2
    )
    return (
        math.pi
        * (semi_major_axis + semi_minor_axis)
        * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))
    )


def calculate_sum_of_n_power_four(n: int) -> int:
    """
    Calculate the sum of the first n natural numbers raised to the power of 4.

    :param n: The number of terms in the series.
    :return: The sum of the series.
    """
    return sum(i**4 for i in range(1, n + 1))


def calculate_spherical_crown_volume(r: float, h: float) -> float:
    """
    Calculate the volume of a spherical crown, given its radius and height.

    :param r: The radius of the base of the spherical crown.
    :param h: The height of the spherical crown.
    :return: The volume of the spherical crown.
    """
    from math import pi

    return (1 / 6) * pi * h * (3 * r**2 + h**2)


def calculate_circular_trapezoid_area(a: float, b: float, h: float) -> float:
    """
    Calculate the area of a circular trapezoid, given the lengths of its bases and height.

    :param a: The length of the smaller base of the trapezoid.
    :param b: The length of the larger base of the trapezoid.
    :param h: The height of the trapezoid.
    :return: The area of the circular trapezoid.
    """
    return 0.5 * (a + b) * h


def calculate_pentagonal_number(n: int) -> int:
    """
    Calculate the nth pentagonal number.

    :param n: The term of the pentagonal number to calculate.
    :return: The nth pentagonal number.
    """
    return n * (3 * n - 1) // 2


def calculate_cycloid_arc_length(r: float, theta: float) -> float:
    """
    Calculate the arc length of a cycloid, given the radius of the generating circle and the angle in radians.

    :param r: The radius of the generating circle.
    :param theta: The angle in radians.
    :return: The arc length of the cycloid.
    """
    from math import sin

    return 4 * r * sin(theta / 2)


def calculate_sum_of_power_series(a: float, r: float, n: int) -> float:
    """
    Calculate the sum of a power series given the first term, common ratio, and number of terms.

    :param a: The first term of the power series.
    :param r: The common ratio between terms in the series.
    :param n: The number of terms in the series.
    :return: The sum of the first n terms of the power series.
    """
    return a * (1 - r**n) / (1 - r)


def calculate_surface_area_of_regular_dipyramid(
    side_length: float, slant_height: float
) -> float:
    """
    Calculate the surface area of a regular dipyramid, i.e.,
    a polyhedron formed by joining two congruent pyramids base-to-base.

    :param side_length: The length of one side of the base polygon.
    :param slant_height: The slant height of the pyramid.
    :return: The total surface area of the regular dipyramid.
    """
    base_perimeter = side_length * 3  # Assuming the base is a triangle for simplicity
    return base_perimeter * slant_height


def calculate_circular_helix_length(radius: float, pitch: float, turns: int) -> float:
    """
    Calculate the length of a circular helix given its radius, pitch, and number of turns.

    :param radius: The radius of the helix.
    :param pitch: The pitch of the helix (height of one complete turn).
    :param turns: The total number of turns in the helix.
    :return: The length of the circular helix.
    """
    from math import pi, sqrt

    return sqrt((2 * pi * radius) ** 2 + pitch**2) * turns


def calculate_volume_of_oblique_cylinder(base_radius: float, height: float) -> float:
    """
    Calculate the volume of an oblique cylinder.

    :param base_radius: The radius of the base of the cylinder.
    :param height: The height of the cylinder measured along the perpendicular from the base to the top.
    :return: The volume of the oblique cylinder.
    """
    from math import pi

    return pi * base_radius**2 * height


def calculate_tetrahedral_number(n: int) -> int:
    """
    Calculate the nth tetrahedral number, which represents the number of spheres in a tetrahedral pyramid.

    :param n: The position in the sequence of tetrahedral numbers.
    :return: The nth tetrahedral number.
    """
    return n * (n + 1) * (n + 2) // 6


def calculate_sum_of_n_power_five(n: int) -> int:
    """
    Calculate the sum of the first n natural numbers raised to the power of five.

    :param n: The number of terms in the series.
    :return: The sum of the series.
    """
    return sum(i**5 for i in range(1, n + 1))


def calculate_spherical_segment_volume(radius: float, height: float) -> float:
    """
    Calculate the volume of a spherical segment.

    :param radius: The radius of the sphere.
    :param height: The height of the spherical segment.
    :return: The volume of the spherical segment.
    """
    from math import pi

    return (pi * height**2) * (3 * radius - height) / 3


def calculate_cosine_wave_amplitude(frequency: float, time: float) -> float:
    """
    Calculate the amplitude of a cosine wave at a given time.

    :param frequency: The frequency of the cosine wave.
    :param time: The time at which to calculate the amplitude.
    :return: The amplitude of the cosine wave.
    """
    from math import cos, pi

    return cos(2 * pi * frequency * time)


def calculate_volume_of_regular_octahedron(edge_length: float) -> float:
    """
    Calculate the volume of a regular octahedron.

    :param edge_length: The length of an edge of the octahedron.
    :return: The volume of the octahedron.
    """
    return (2 * (edge_length**3)) / (3 * (2**0.5))


def calculate_sum_of_inverse_squares(n: int) -> float:
    """
    Calculate the sum of the inverse squares of the first n natural numbers.

    :param n: The number of terms in the series.
    :return: The sum of the series.
    """
    return sum(1 / i**2 for i in range(1, n + 1))


def calculate_sum_of_n_power_six(n: int) -> int:
    """
    Calculate the sum of the first n natural numbers raised to the power of six.

    :param n: The number of terms in the series.
    :return: The sum of the series.
    """
    return sum(i**6 for i in range(1, n + 1))


def calculate_spherical_shell_mass(
    density: float, outer_radius: float, inner_radius: float
) -> float:
    """
    Calculate the mass of a spherical shell given its density and inner/outer radii.

    :param density: The density of the material of the spherical shell.
    :param outer_radius: The outer radius of the spherical shell.
    :param inner_radius: The inner radius of the spherical shell.
    :return: The mass of the spherical shell.
    """
    from math import pi

    volume = (4 / 3) * pi * (outer_radius**3 - inner_radius**3)
    return density * volume


def calculate_velocity_final(
    velocity_initial: float, acceleration: float, time: float
) -> float:
    """
    Calculate the final velocity of an object given its initial velocity, acceleration, and time.

    :param velocity_initial: The initial velocity of the object.
    :param acceleration: The acceleration of the object.
    :param time: The time over which the acceleration is applied.
    :return: The final velocity of the object.
    """
    return velocity_initial + acceleration * time


def calculate_centripetal_force(mass: float, velocity: float, radius: float) -> float:
    """
    Calculate the centripetal force on an object moving in a circle at constant speed.

    :param mass: The mass of the object.
    :param velocity: The velocity of the object.
    :param radius: The radius of the circle along which the object is moving.
    :return: The centripetal force exerted on the object.
    """
    return mass * (velocity**2) / radius


def calculate_bernoulli_number(n: int) -> float:
    """
    Calculate the nth Bernoulli number using the recursive formula.

    Note: This implementation is not optimized for large values of n due to its recursive nature.

    :param n: The order of the Bernoulli number to calculate.
    :return: The nth Bernoulli number.
    """
    if n == 0:
        return 1
    if n == 1:
        return -0.5
    if n % 2 != 0:
        return 0
    a = [0] * (n + 1)
    for m in range(n + 1):
        a[m] = 1 / (m + 1)
        for j in range(m, 0, -1):
            a[j - 1] = j * (a[j - 1] - a[j])
    return a[0] - 1


def calculate_sum_of_n_triangular_numbers(n: int) -> int:
    """
    Calculate the sum of the first n triangular numbers.

    :param n: The number of triangular numbers to sum up.
    :return: The sum of the first n triangular numbers.
    """
    return n * (n + 1) * (n + 2) // 6


def calculate_surface_area_of_spherical_sector(radius: float, height: float) -> float:
    """
    Calculate the surface area of a spherical sector.

    :param radius: The radius of the sphere.
    :param height: The height of the spherical cap.
    :return: The surface area of the spherical sector.
    """
    from math import pi

    return 2 * pi * radius * height


def calculate_sum_of_n_powers(n: int, power: int) -> int:
    """
    Calculate the sum of the first n natural numbers raised to a given power.

    :param n: The number of terms.
    :param power: The power to which each term is raised.
    :return: The sum of the first n natural numbers raised to the specified power.
    """
    return sum([i**power for i in range(1, n + 1)])


def calculate_surface_area_of_spherical_zone(radius: float, height: float) -> float:
    """
    Calculate the surface area of a spherical zone.
    The formula used is: A = 2 * pi * r * h
    where r is the radius of the sphere, and h is the height of the zone.

    :param radius: The radius of the sphere from which the zone is a part.
    :param height: The height of the spherical zone.
    :return: The surface area of the spherical zone.
    """
    import math

    return 2 * math.pi * radius * height


def calculate_cosine_of_angle(angle_in_degrees: float) -> float:
    """
    Calculate the cosine of an angle given in degrees.
    This function uses the math library to convert the angle from degrees to radians
    and then calculates the cosine.

    :param angle_in_degrees: The angle in degrees for which to calculate the cosine.
    :return: The cosine of the given angle.
    """
    import math

    angle_in_radians = math.radians(angle_in_degrees)
    return math.cos(angle_in_radians)


def calculate_sine_of_angle(angle_in_degrees: float) -> float:
    """
    Calculate the sine of an angle given in degrees.
    This function uses the math library to convert the angle from degrees to radians
    and then calculates the sine.

    :param angle_in_degrees: The angle in degrees for which to calculate the sine.
    :return: The sine of the given angle.
    """
    import math

    angle_in_radians = math.radians(angle_in_degrees)
    return math.sin(angle_in_radians)


def calculate_tangent_of_angle(angle_in_degrees: float) -> float:
    """
    Calculate the tangent of an angle given in degrees.
    This function uses the math library to convert the angle from degrees to radians
    and then calculates the tangent.

    :param angle_in_degrees: The angle in degrees for which to calculate the tangent.
    :return: The tangent of the given angle.
    """
    import math

    angle_in_radians = math.radians(angle_in_degrees)
    return math.tan(angle_in_radians)


def calculate_cotangent_of_angle(angle_in_degrees: float) -> float:
    """
    Calculate the cotangent of an angle given in degrees.
    This function calculates the cotangent by taking the reciprocal of the tangent
    of the angle, which is converted from degrees to radians.

    :param angle_in_degrees: The angle in degrees for which to calculate the cotangent.
    :return: The cotangent of the given angle.
    """
    import math

    angle_in_radians = math.radians(angle_in_degrees)
    return 1 / math.tan(angle_in_radians)


def calculate_sum_of_sine_series(x: float, n: int) -> float:
    """
    Calculate the sum of the first 'n' terms of the sine series for a given angle 'x' (in radians).

    :param x: The angle in radians for which the sine series sum is to be calculated.
    :param n: The number of terms of the sine series to sum up.
    :return: The sum of the first 'n' terms of the sine series for the given angle 'x'.
    """
    from math import factorial, pow

    sum_series = 0
    for i in range(n):
        sign = pow(-1, i)
        sum_series += sign * (pow(x, 2 * i + 1) / factorial(2 * i + 1))
    return sum_series


def calculate_cosine_series_sum(x: float, n: int) -> float:
    """
    Calculate the sum of the first 'n' terms of the cosine series for a given angle 'x' (in radians).

    :param x: The angle in radians for which the cosine series sum is to be calculated.
    :param n: The number of terms of the cosine series to sum up.
    :return: The sum of the first 'n' terms of the cosine series for the given angle 'x'.
    """
    from math import factorial, pow

    sum_series = 0
    for i in range(n):
        sign = pow(-1, i)
        sum_series += sign * (pow(x, 2 * i) / factorial(2 * i))
    return sum_series


def calculate_eulers_number_approximation(n: int) -> float:
    """
    Calculate an approximation of Euler's number 'e' by summing the first 'n' terms of its series expansion.

    :param n: The number of terms to include in the approximation of Euler's number.
    :return: An approximation of Euler's number 'e' based on the sum of the first 'n' terms of its series.
    """
    from math import factorial

    e_approx = sum(1 / factorial(i) for i in range(n))
    return e_approx


def calculate_sum_of_powers_of_x(x: float, n: int) -> float:
    """
    Calculate the sum of the first 'n' powers of 'x', starting from x^0 to x^(n-1).

    :param x: The base number whose powers are to be summed.
    :param n: The number of terms (powers of 'x') to include in the sum.
    :return: The sum of the first 'n' powers of 'x'.
    """
    return sum(x**i for i in range(n))


def calculate_leibniz_pi_approximation(n: int) -> float:
    """
    Calculate an approximation of Pi using the Leibniz formula for π.

    :param n: The number of terms to include in the approximation of Pi.
    :return: An approximation of Pi based on the Leibniz formula.
    """
    pi_approx = sum((-1) ** k / (2 * k + 1) for k in range(n)) * 4
    return pi_approx


# calculus


def calculate_integral_of_polynomial(
    coefficients: list[float], variable: str = "x"
) -> str:
    """
    Calculate the indefinite integral of a polynomial function.
    The function calculates the indefinite integral of a polynomial function given its coefficients.
    The coefficients should be provided in a list, starting from the highest degree to the constant term.
    The function returns a string that represents the indefinite integral of the polynomial.

    :param coefficients: A list of coefficients from the highest degree to the constant term.
    :param variable: The variable used in the polynomial function.
    :return: A string representation of the indefinite integral of the polynomial.
    """
    integral = ""
    degree = len(coefficients)
    for i, coef in enumerate(coefficients):
        if coef == 0:
            continue
        new_coef = coef / (degree - i)
        if integral:
            integral += " + " if new_coef > 0 else " - "
        integral += (
            f"{abs(new_coef)}{variable}^{degree - i}"
            if degree - i - 1 != 0
            else f"{abs(new_coef)}"
        )
    integral += " + C"
    return integral


def calculate_derivative_of_polynomial(coefficients: list[float]) -> list:
    """
    Calculate the derivative of a polynomial function.

    This function calculates the derivative of a polynomial function given its coefficients.
    The coefficients should be provided in a list, starting from the highest degree to the constant term.
    The function returns a list of coefficients that represent the derivative of the polynomial.

    :param coefficients: A list of coefficients from the highest degree to the constant term.
    :return: A list of coefficients representing the derivative of the polynomial.
    """
    derivative = [i * coef for i, coef in enumerate(coefficients)][1:]
    return derivative


def calculate_exponential_growth(
    initial_amount: float, growth_rate: float, time: float
) -> float:
    """
    Calculate the exponential growth based on an initial amount, a growth rate, and time.

    :param initial_amount: The initial amount before growth.
    :param growth_rate: The rate of growth per time period.
    :param time: The time period over which the growth is calculated.
    :return: The amount after growth over the specified time period.
    """
    return initial_amount * (1 + growth_rate) ** time


def calculate_logarithmic_growth(value: float, base: float) -> float:
    """
    Calculate the logarithm of a value with a specified base.

    :param value: The value to calculate the logarithm for.
    :param base: The base of the logarithm.
    :return: The logarithm of the value with the specified base.
    """
    import math

    return math.log(value, base)


def calculate_derivative_of_exponential_function(
    base: float, exponent: float, at_point: float
) -> float:
    """
    Calculate the derivative of an exponential function at a given point.

    :param base: The base of the exponential function.
    :param exponent: The exponent of the exponential function.
    :param at_point: The point at which to calculate the derivative.
    :return: The value of the derivative at the specified point.
    """
    import math

    return (base**at_point) * math.log(base) * exponent


def calculate_derivative_of_log(x: float) -> float:
    """
    Calculate the derivative of the natural logarithm function at a given point.

    :param x: The point at which to evaluate the derivative of the natural logarithm.
    :return: The value of the derivative of the natural logarithm at the given point.
    """
    return 1 / x


def calculate_volume_of_parallelepiped_from_sides(
    a: float, b: float, c: float, angle: float
) -> float:
    """
    Calculate the volume of a parallelepiped given sides and the angle between them.

    :param a: Length of the first side.
    :param b: Length of the second side.
    :param c: Length of the third side.
    :param angle: Angle between sides a and b in radians.
    :return: The volume of the parallelepiped.
    """
    from math import sin

    return a * b * c * sin(angle)


def calculate_integral_of_sin(x: float) -> float:
    """
    Calculate the indefinite integral of the sine function.

    :param x: The upper limit of integration.
    :return: The value of the indefinite integral of sine from 0 to x.
    """
    from math import cos

    return -cos(x) + cos(0)


def calculate_euler_number_power(x: float) -> float:
    """
    Calculate the value of the Euler's number (e) raised to the power of x.

    :param x: The exponent to which Euler's number is raised.
    :return: The value of e^x.
    """
    from math import exp

    return exp(x)


def calculate_derivative_of_trig_function(function: str, at_point: float) -> float:
    """
    Calculate the derivative of a trigonometric function at a given point.

    :param function: A string representing the trigonometric function. Supported functions are 'sin', 'cos', and 'tan'.
    :param at_point: The point at which to evaluate the derivative.
    :return: The value of the derivative at the specified point.
    """
    import math

    if function == "sin":
        return math.cos(at_point)
    elif function == "cos":
        return -math.sin(at_point)
    elif function == "tan":
        return 1 / (math.cos(at_point) ** 2)
    else:
        raise ValueError("Unsupported function. Please use 'sin', 'cos', or 'tan'.")


def calculate_volume_of_paraboloid(height: float, radius: float) -> float:
    """
    Calculate the volume of a paraboloid based on its height and radius.

    :param height: The height of the paraboloid.
    :param radius: The radius of the base of the paraboloid.
    :return: The volume of the paraboloid.
    """
    import math

    return (1 / 2) * math.pi * (radius**2) * height


def calculate_surface_area_of_hemisphere(radius: float) -> float:
    """
    Calculate the surface area of a hemisphere given its radius.

    :param radius: The radius of the hemisphere.
    :return: The surface area of the hemisphere.
    """
    import math

    return 3 * math.pi * (radius**2)


def calculate_exponential_decay(
    initial_amount: float, decay_rate: float, time: float
) -> float:
    """
    Calculate the remaining amount after exponential decay over a period of time.

    :param initial_amount: The initial amount before decay.
    :param decay_rate: The rate of decay, where 0 < decay_rate < 1.
    :param time: The time over which the decay occurs.
    :return: The remaining amount after decay.
    """
    import math

    return initial_amount * math.exp(-decay_rate * time)


def calculate_hyperbolic_sine(x: float) -> float:
    """
    Calculate the hyperbolic sine of a given value.

    :param x: The value to calculate the hyperbolic sine for.
    :return: The hyperbolic sine of x.
    """
    import math

    return (math.exp(x) - math.exp(-x)) / 2


def calculate_volume_of_regular_dodecahedron(side_length: float) -> float:
    """
    Calculate the volume of a regular dodecahedron.

    :param side_length: The length of a side of the dodecahedron.
    :return: The volume of the regular dodecahedron.
    """
    return (15 + 7 * 5**0.5) / 4 * side_length**3


def calculate_surface_area_of_circular_cone(
    radius: float, slant_height: float
) -> float:
    """
    Calculate the surface area of a circular cone.

    :param radius: The radius of the base of the cone.
    :param slant_height: The slant height of the cone.
    :return: The surface area of the circular cone.
    """
    import math

    return math.pi * radius * (radius + slant_height)


def calculate_volume_of_regular_hexahedron(side_length: float) -> float:
    """
    Calculate the volume of a regular hexahedron (cube).

    :param side_length: The length of a side of the hexahedron.
    :return: The volume of the hexahedron.
    """
    return side_length**3


def calculate_spherical_shell_volume(outer_radius: float, inner_radius: float) -> float:
    """
    Calculate the volume of a spherical shell.

    :param outer_radius: The outer radius of the spherical shell.
    :param inner_radius: The inner radius of the spherical shell.
    :return: The volume of the spherical shell.
    """
    import math

    return (4 / 3) * math.pi * (outer_radius**3 - inner_radius**3)


def calculate_surface_area_of_circular_cylinder(radius: float, height: float) -> float:
    """
    Calculate the surface area of a circular cylinder.

    :param radius: The radius of the circular base of the cylinder.
    :param height: The height of the cylinder.
    :return: The surface area of the circular cylinder.
    """
    import math

    return 2 * math.pi * radius * (radius + height)


def calculate_circular_cone_lateral_surface_area(
    radius: float, slant_height: float
) -> float:
    """
    Calculate the lateral surface area of a circular cone.

    :param radius: The radius of the base of the cone.
    :param slant_height: The slant height of the cone.
    :return: The lateral surface area of the circular cone.
    """
    import math

    return math.pi * radius * slant_height


def calculate_exponential_function(base: float, exponent: float) -> float:
    """
    Calculate the value of a base raised to a given exponent.

    :param base: The base of the exponential function.
    :param exponent: The exponent to which the base is raised.
    :return: The calculated value of base raised to the exponent.
    """
    return base**exponent


def calculate_natural_logarithm(value: float) -> float:
    """
    Calculate the natural logarithm of a given value.

    :param value: The value to calculate the natural logarithm for.
    :return: The natural logarithm of the given value.
    """
    import math

    return math.log(value)


def calculate_area_of_regular_hexagon(side_length: float) -> float:
    """
    Calculate the area of a regular hexagon given the length of its sides.

    :param side_length: The length of each side of the hexagon.
    :return: The area of the regular hexagon.
    """
    return (3 * (3**0.5) * (side_length**2)) / 2


def calculate_volume_of_pyramidal_frustum(
    top_side_length: float, base_side_length: float, height: float
) -> float:
    """
    Calculate the volume of a pyramidal frustum given the lengths of the top and base sides, and its height.

    :param top_side_length: The length of the top side of the pyramidal frustum.
    :param base_side_length: The length of the base side of the pyramidal frustum.
    :param height: The height of the pyramidal frustum.
    :return: The volume of the pyramidal frustum.
    """
    return (height / 3) * (
        top_side_length**2 + base_side_length**2 + (top_side_length * base_side_length)
    )


def calculate_surface_area_of_spheroid(a: float, b: float) -> float:
    """
    Calculate the surface area of a spheroid.

    :param a: semi-major axis of the spheroid
    :param b: semi-minor axis of the spheroid
    :return: surface area of the spheroid
    """
    from math import asin, log, pi, sqrt

    if a == b:  # Sphere
        return 4 * pi * a**2
    elif a > b:  # Oblate spheroid
        e = sqrt(1 - (b**2 / a**2))
        return 2 * pi * a**2 * (1 + (1 - e**2) / e * log((1 + e) / (1 - e)) / 2)
    else:  # Prolate spheroid
        e = sqrt(1 - (a**2 / b**2))
        return 2 * pi * a**2 * (1 + b / (a * e) * asin(e))


def calculate_volume_of_spheroid(a: float, b: float) -> float:
    """
    Calculate the volume of a spheroid.

    :param a: semi-major axis of the spheroid
    :param b: semi-minor axis of the spheroid
    :return: volume of the spheroid
    """
    from math import pi

    return 4 / 3 * pi * a**2 * b


def calculate_taylor_series_expansion(x: float, n: int) -> float:
    """
    Calculate the Taylor series expansion of e^x up to n terms.

    :param x: the exponent
    :param n: number of terms in the Taylor series
    :return: approximation of e^x using Taylor series
    """
    from math import factorial

    return sum(x**i / factorial(i) for i in range(n))


def calculate_circular_sector_area(radius: float, angle: float) -> float:
    """
    Calculate the area of a circular sector.

    :param radius: radius of the circle
    :param angle: angle of the sector in radians
    :return: area of the circular sector
    """
    from math import pi

    return (angle / (2 * pi)) * pi * radius**2


def calculate_partial_derivative_quadratic(x: float, y: float) -> float:
    """
    Calculate the partial derivative of a quadratic function with respect to x.

    The quadratic function is defined as f(x, y) = 3x^2 + 4xy + 5y^2.

    :param x: The x-value at which to calculate the partial derivative.
    :param y: The y-value used in the partial derivative calculation.
    :return: The value of the partial derivative with respect to x at point (x, y).
    """
    return 6 * x + 4 * y


def calculate_surface_area_of_circular_ring(
    inner_radius: float, outer_radius: float
) -> float:
    """
    Calculate the surface area of a circular ring given its inner and outer radii.

    :param inner_radius: The radius of the inner circle of the ring.
    :param outer_radius: The radius of the outer circle of the ring.
    :return: The surface area of the circular ring.
    """
    import math

    return math.pi * (outer_radius**2 - inner_radius**2)


def calculate_velocity_average(
    initial_velocity: float, final_velocity: float, time: float
) -> float:
    """
    Calculate the average velocity over a time period given the initial and final velocities.

    :param initial_velocity: The velocity at the beginning of the time period.
    :param final_velocity: The velocity at the end of the time period.
    :param time: The time period over which the average is calculated.
    :return: The average velocity.
    """
    return (final_velocity - initial_velocity) / time


def calculate_acceleration(
    initial_velocity: float, final_velocity: float, time: float
) -> float:
    """
    Calculate the acceleration given the initial and final velocities and the time period over which the change occurs.

    :param initial_velocity: The velocity at the beginning of the time period.
    :param final_velocity: The velocity at the end of the time period.
    :param time: The time period over which the acceleration occurs.
    :return: The acceleration.
    """
    return (final_velocity - initial_velocity) / time


def calculate_elliptic_arc_length(a: float, b: float, phi: float) -> float:
    """
    Calculate the length of an elliptic arc given the semi-major axis, semi-minor axis,
    and the central angle in radians.

    :param a: The semi-major axis of the ellipse.
    :param b: The semi-minor axis of the ellipse.
    :param phi: The central angle of the arc in radians.
    :return: The approximate length of the elliptic arc.
    """
    import math

    h = ((a - b) ** 2) / ((a + b) ** 2)
    return math.pi * (a + b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h))) * phi


def calculate_triple_integral(
    func,
    x_range: tuple[float, ...],
    y_range: tuple[float, ...],
    z_range: tuple[float, ...],
) -> float:
    """
    Calculate the triple integral of a given function over specified ranges.

    :param func: A function of three variables (x, y, z) to integrate over.
    :param x_range: A tuple (start, end) defining the range of x.
    :param y_range: A tuple (start, end) defining the range of y.
    :param z_range: A tuple (start, end) defining the range of z.
    :return: The numerical value of the triple integral.
    """
    from scipy.integrate import tplquad

    return tplquad(
        func,
        x_range[0],
        x_range[1],
        lambda x: y_range[0],
        lambda x: y_range[1],
        lambda x, y: z_range[0],
        lambda x, y: z_range[1],
    )[0]


def calculate_volume_of_spherical_sector(radius: float, height: float) -> float:
    """
    Calculate the volume of a spherical sector given its radius and height.

    :param radius: The radius of the sphere.
    :param height: The height of the spherical sector.
    :return: The volume of the spherical sector.
    """
    from math import pi

    return (1 / 3) * pi * height**2 * (3 * radius - height)


def calculate_length_of_vector(vector: tuple[float, ...]) -> float:
    """
    Calculate the length (magnitude) of a vector in n-dimensional space.

    :param vector: A tuple representing the vector components.
    :return: The length of the vector.
    """
    from math import sqrt

    return sqrt(sum(comp**2 for comp in vector))


def calculate_volume_of_spherical_cap(radius: float, height: float) -> float:
    """
    Calculate the volume of a spherical cap.

    :param radius: The radius of the sphere from which the cap is a part.
    :param height: The height of the cap.
    :return: The volume of the spherical cap.
    """
    from math import pi

    return (1 / 3) * pi * height**2 * (3 * radius - height)


def calculate_length_of_spiral_on_cone(
    base_radius: float, height: float, number_of_turns: float
) -> float:
    """
    Calculate the length of a spiral on a cone.

    :param base_radius: The base radius of the cone.
    :param height: The height of the cone.
    :param number_of_turns: The number of turns the spiral makes around the cone.
    :return: The length of the spiral.
    """
    import math

    return math.sqrt((2 * math.pi * base_radius * number_of_turns) ** 2 + height**2)


def calculate_area_of_hyperbolic_sector(a: float, b: float, theta: float) -> float:
    """
    Calculate the area of a hyperbolic sector.

    :param a: The semi-major axis of the hyperbola.
    :param b: The semi-minor axis of the hyperbola.
    :param theta: The angle in radians subtended by the sector at the hyperbola's center.
    :return: The area of the hyperbolic sector.
    """
    return 0.5 * a * b * theta


def calculate_torus_knot_length(
    radius: float, tube_radius: float, p: int, q: int
) -> float:
    """
    Calculate the length of a torus knot.

    :param radius: The major radius of the torus.
    :param tube_radius: The radius of the tube.
    :param p: The number of times the knot wraps around the axis of rotational symmetry.
    :param q: The number of times the knot wraps through the hole of the torus.
    :return: The length of the torus knot.
    """
    import math

    return (
        2
        * math.pi
        * math.sqrt(
            (radius + tube_radius * math.cos(p / q * 2 * math.pi)) ** 2
            + (tube_radius * math.sin(p / q * 2 * math.pi)) ** 2
        )
        * q
    )


def calculate_surface_area_of_regular_pyramid(
    base_area: float, slant_height: float
) -> float:
    """
    Calculate the surface area of a regular pyramid.

    :param base_area: The area of the base of the pyramid.
    :param slant_height: The slant height of the pyramid.
    :return: The total surface area of the pyramid.
    """
    perimeter = (4 * base_area) ** 0.5  # Assuming the base is a square for simplicity
    return base_area + 0.5 * perimeter * slant_height


def calculate_circumradius_of_regular_polygon(
    side_length: float, num_sides: int
) -> float:
    """
    Calculate the circumradius of a regular polygon.

    :param side_length: The length of a side of the polygon.
    :param num_sides: The number of sides of the polygon.
    :return: The circumradius of the polygon.
    """
    from math import pi, sin

    return side_length / (2 * sin(pi / num_sides))


def calculate_circle_radius_inscribed_in_polygon(
    area: float, perimeter: float
) -> float:
    """
    Calculate the radius of an inscribed circle in a polygon.

    :param area: The area of the polygon.
    :param perimeter: The perimeter of the polygon.
    :return: The radius of the inscribed circle.
    """
    return area / perimeter


def calculate_circumference_of_polygon(side_length: float, num_sides: int) -> float:
    """
    Calculate the circumference of a regular polygon.

    :param side_length: The length of one side of the polygon.
    :param num_sides: The number of sides of the polygon.
    :return: The circumference of the polygon.
    """
    return side_length * num_sides


def calculate_elliptic_integral_of_first_kind(phi: float, k: float) -> float:
    """
    Calculate the elliptic integral of the first kind.

    :param phi: The amplitude of the elliptic integral.
    :param k: The modulus of the elliptic integral.
    :return: The value of the elliptic integral of the first kind.
    """
    from scipy.special import ellipkinc

    return ellipkinc(phi, k)


def calculate_area_of_regular_polygon(side_length: float, num_sides: int) -> float:
    """
    Calculate the area of a regular polygon.

    :param side_length: The length of one side of the polygon.
    :param num_sides: The number of sides of the polygon.
    :return: The area of the regular polygon.
    """
    from math import pi, tan

    return (num_sides * side_length**2) / (4 * tan(pi / num_sides))


def calculate_ellipsoid_volume(a: float, b: float, c: float) -> float:
    """
    Calculate the volume of an ellipsoid.

    :param a: The semi-axis length in the x-direction.
    :param b: The semi-axis length in the y-direction.
    :param c: The semi-axis length in the z-direction.
    :return: The volume of the ellipsoid.
    """
    from math import pi

    return (4 / 3) * pi * a * b * c


def calculate_circumference_of_regular_polygon(
    side_length: float, num_sides: int
) -> float:
    """
    Calculate the circumference of a regular polygon.

    :param side_length: The length of one side of the polygon.
    :param num_sides: The number of sides of the polygon.
    :return: The circumference of the polygon.
    """
    return side_length * num_sides


def calculate_tangent_of_hyperbola(x: float) -> float:
    """
    Calculate the tangent of a hyperbola at a given point.

    :param x: The x-coordinate of the point on the hyperbola.
    :return: The tangent of the hyperbola at the given point.
    """
    return 1 / x


def calculate_exponential_integral(x: float) -> float:
    """
    Calculate the exponential integral of a given value.

    :param x: The value to calculate the exponential integral for.
    :return: The exponential integral of the given value.
    """
    from scipy.integrate import quad

    return quad(lambda t: (1 / t) * (1 / (1 + x / t)), 1, float("inf"))


def calculate_logarithmic_integral(x: float) -> float:
    """
    Calculate the logarithmic integral of a given value.

    :param x: The value to calculate the logarithmic integral for.
    :return: The logarithmic integral of the given value.
    """
    import numpy as np
    from scipy.integrate import quad

    return quad(lambda t: 1 / np.log(t), 2, x)


def calculate_surface_area_of_circular_disk(radius: float) -> float:
    """
    Calculate the surface area of a circular disk.

    :param radius: The radius of the circular disk.
    :return: The surface area of the circular disk.
    """
    import math

    return math.pi * radius**2


def calculate_triple_angle_formula_sin(angle: float) -> float:
    """
    Calculate the sine of three times the given angle using the triple angle formula.

    :param angle: The angle in radians.
    :return: The sine of three times the angle.
    """
    from math import sin

    return 3 * sin(angle) - 4 * sin(angle) ** 3


def calculate_triple_angle_formula_cos(angle: float) -> float:
    """
    Calculate the cosine of three times the given angle using the triple angle formula.

    :param angle: The angle in radians.
    :return: The cosine of three times the angle.
    """
    from math import cos

    return 4 * cos(angle) ** 3 - 3 * cos(angle)


def calculate_surface_area_of_regular_octagon(side_length: float) -> float:
    """
    Calculate the surface area of a regular octagon given the length of one side.

    :param side_length: The length of one side of the octagon.
    :return: The surface area of the octagon.
    """
    return 2 * (1 + 2**0.5) * side_length**2


def calculate_circumference_of_regular_dodecahedron(side_length: float) -> float:
    """
    Calculate the circumference of a regular dodecahedron given the length of one side.

    :param side_length: The length of one side of the dodecahedron.
    :return: The circumference of the dodecahedron.
    """
    return 30 * side_length


# number_theory


def is_prime(n: int) -> bool:
    """
    Check if a given number is prime.

    A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.

    :param n: The number to check for primality.
    :return: True if n is a prime number, False otherwise.
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def euler_phi(n: int) -> int:
    """
    Calculate Euler's Totient Function (phi) for a given positive integer.

    Euler's Totient Function counts the positive integers up to a given integer n that are relatively prime to n.

    :param n: A positive integer to calculate the totient function for.
    :return: The value of Euler's Totient Function for n.
    """
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result


def is_perfect_number(n: int) -> bool:
    """
    Check if a given number is a perfect number.

    A perfect number is a positive integer that is equal to the sum of its proper divisors,
    excluding the number itself.

    :param n: The number to check.
    :return: True if n is a perfect number, False otherwise.
    """
    if n < 2:
        return False
    return sum_of_divisors(n) - n == n


def is_coprime(a: int, b: int) -> bool:
    """
    Check if two numbers are coprime.

    Two numbers are coprime if their greatest common divisor (GCD) is 1.

    :param a: First number
    :param b: Second number
    :return: True if a and b are coprime, False otherwise
    """
    while b:
        a, b = b, a % b
    return a == 1


def modular_exponentiation(base: int, exponent: int, modulus: int) -> int:
    """
    Perform modular exponentiation.

    Calculate base^exponent mod modulus efficiently.

    :param base: The base number
    :param exponent: The exponent
    :param modulus: The modulus
    :return: The result of (base^exponent) mod modulus
    """
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result


def mobius_function(n: int) -> int:
    """
    Calculate the Möbius function.

    The Möbius function is defined as:
    1 if n is a square-free positive integer with an even number of prime factors.
    -1 if n is a square-free positive integer with an odd number of prime factors.
    0 if n has a squared prime factor.

    :param n: The input number
    :return: The value of the Möbius function for n
    """
    if n == 1:
        return 1
    prime_factors = set()
    for i in range(2, int(n**0.5) + 1):
        while n % i == 0:
            prime_factors.add(i)
            n //= i
            if n % i == 0:
                return 0
    if n > 1:
        prime_factors.add(n)
    return -1 if len(prime_factors) % 2 else 1


def is_square(n: int) -> bool:
    """
    Check if a number is a perfect square.

    :param n: The number to check.
    :return: True if n is a perfect square, False otherwise.
    """
    return int(n**0.5) ** 2 == n


def digital_root(n: int) -> int:
    """
    Calculate the digital root of a number.

    The digital root is the recursive sum of all the digits in a number.
    Given n, repeatedly add all its digits until the result has only one digit.

    :param n: The number to calculate the digital root of.
    :return: The digital root of n.
    """
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n


def euler_phi_n_up_to(n: int) -> list:
    """
    Calculate Euler's Totient function φ(n) for all numbers from 1 to n.

    Euler's Totient function, φ(n), is defined as the number of positive integers
    less than or equal to n that are coprime to n.

    :param n: The upper limit of the range to calculate φ(n) for.
    :return: A list of values of φ(n) for all numbers from 1 to n.
    """
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i
    return phi


def sum_of_proper_divisors(n: int) -> int:
    """
    Calculate the sum of all proper divisors of a number.

    A proper divisor of a number is a divisor that is strictly less than the number.

    :param n: The number to calculate the sum of proper divisors for.
    :return: The sum of all proper divisors of n.
    """
    divisors_sum = 1  # 1 is a proper divisor of every number
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors_sum += i
            if i != n // i:  # Avoid adding the square root twice for perfect squares
                divisors_sum += n // i
    return divisors_sum


def aliquot_sequence(n: int, length: int) -> list:
    """
    Generate a sequence of numbers where each number is the sum of the proper divisors of the previous number.

    :param n: The starting number of the sequence.
    :param length: The length of the sequence to generate.
    :return: A list representing the aliquot sequence starting at n of the specified length.
    """
    sequence = [n]
    for _ in range(1, length):
        n = sum_of_proper_divisors(n)
        sequence.append(n)
    return sequence


def is_palindrome_number(n: int) -> bool:
    """
    Check if a given number is a palindrome.

    :param n: The number to check.
    :return: True if n is a palindrome, False otherwise.
    """
    return str(n) == str(n)[::-1]


def calculate_digit_sum(n: int) -> int:
    """
    Calculate the sum of the digits of a given number.

    :param n: The number whose digit sum is to be calculated.
    :return: The sum of the digits of n.
    """
    return sum(int(digit) for digit in str(n))


def is_armstrong_number(n: int) -> bool:
    """
    Check if a given number is an Armstrong number.

    An Armstrong number is a number that is the sum of its own digits each raised to the power of the number of digits.

    :param n: The number to check.
    :return: True if n is an Armstrong number, False otherwise.
    """
    digits = [int(digit) for digit in str(n)]
    return sum(digit ** len(digits) for digit in digits) == n


def calculate_num_divisors(n: int) -> int:
    """
    Calculate the number of divisors of a given number.

    :param n: The number whose divisors are to be calculated.
    :return: The number of divisors of n.
    """
    divisors = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors += 2 if i != n // i else 1
    return divisors


def is_abundant_number(n: int) -> bool:
    """
    Check if a given number is abundant.

    An abundant number is a number for which the sum of its proper divisors is greater than the number itself.

    :param n: The number to check.
    :return: True if n is abundant, False otherwise.
    """
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum > n


def is_deficient_number(n: int) -> bool:
    """
    Check if a number is deficient.

    A number is considered deficient if the sum of its proper divisors
    is less than the number itself.

    :param n: The number to check.
    :return: True if the number is deficient, False otherwise.
    """
    divisors_sum = sum([i for i in range(1, n) if n % i == 0])
    return divisors_sum < n


def calculate_totatives(n: int) -> list:
    """
    Calculate the totatives of a given number.

    A totative is a positive integer less than or equal to a number which is
    relatively prime to the number. The function returns a list of all totatives.

    :param n: The number to find totatives for.
    :return: A list of totatives of the given number.
    """
    return [i for i in range(1, n + 1) if gcd(i, n) == 1]


def gcd(a: int, b: int) -> int:
    """
    Calculate the greatest common divisor (GCD) of two numbers.

    The GCD of two numbers is the largest positive integer that divides each of the integers.

    :param a: First number.
    :param b: Second number.
    :return: The greatest common divisor of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def is_semiprime(n: int) -> bool:
    """
    Check if a number is a semiprime.

    A semiprime is a natural number that is the product of two prime numbers.
    This function returns True if the given number is a semiprime, False otherwise.

    :param n: The number to check.
    :return: True if the number is a semiprime, False otherwise.
    """
    prime_factors = 0
    for i in range(2, int(n**0.5) + 1):
        while n % i == 0:
            prime_factors += 1
            n //= i
        if prime_factors > 2:
            return False
    if n > 1:
        prime_factors += 1
    return prime_factors == 2


def is_amicable_number(a: int) -> bool:
    """
    Check if a number is an amicable number.

    An amicable number is a number for which the sum of its proper divisors
    is equal to another number, and the sum of the proper divisors of this
    second number is equal to the first number.

    :param a: The number to check.
    :return: True if the number is an amicable number, False otherwise.
    """
    b = sum_of_divisors(a)
    return a != b and sum_of_divisors(b) == a


def is_perfect_square(n: int) -> bool:
    """
    Check if a number is a perfect square.

    A perfect square is an integer that is the square of an integer.

    :param n: The number to check.
    :return: True if n is a perfect square, False otherwise.
    """
    root = n**0.5
    return int(root + 0.5) ** 2 == n


def is_friendly_pair(a: int, b: int) -> bool:
    """
    Check if two numbers are a friendly pair (amicable numbers but with a different definition).

    Two numbers are a friendly pair if the ratios of the sum of their proper divisors
    to the numbers themselves are equal.

    :param a: First number.
    :param b: Second number.
    :return: True if a and b are a friendly pair, False otherwise.
    """
    sum_a = sum_of_divisors(a)
    sum_b = sum_of_divisors(b)
    return (sum_a / a) == (sum_b / b)


def is_happy_number(n: int) -> bool:
    """
    Determine if a number is a "happy number".

    A happy number is defined as a number which eventually reaches 1 when replaced by
    the sum of the square of each digit.

    :param n: The number to check.
    :return: True if n is a happy number, False otherwise.
    """
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(char) ** 2 for char in str(n))
    return n == 1


def is_carmichael_number(n: int) -> bool:
    """
    Check if a number is a Carmichael number.

    A Carmichael number is a composite number n which satisfies the modular arithmetic condition b^n = b (mod n)
    for all integers b which are relatively prime to n.

    :param n: The number to check.
    :return: True if n is a Carmichael number, False otherwise.
    """
    if n <= 1 or is_prime(n):
        return False
    for b in range(2, n):
        if gcd(b, n) == 1 and pow(b, n - 1, n) != 1:
            return False
    return True


def is_mersenne_prime(p: int) -> bool:
    """
    Check if a number is a Mersenne prime.

    A Mersenne prime is a prime number that is one less than a power of two. It is of the form M_p = 2^p - 1
    where p is also a prime.

    :param p: The exponent to check if 2^p - 1 is a Mersenne prime.
    :return: True if 2^p - 1 is a Mersenne prime, False otherwise.
    """
    if p == 2:
        return True
    m_p = 2**p - 1
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % m_p
    return s == 0


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


def prime_count_up_to(n: int) -> int:
    """
    Count the number of prime numbers less than or equal to n.

    :param n: The upper limit to count prime numbers up to.
    :return: The count of prime numbers less than or equal to n.
    """
    if n < 2:
        return 0
    prime = [True] * (n + 1)
    p = 2
    while p * p <= n:
        if prime[p]:
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1
    prime[0] = False
    prime[1] = False
    return sum(prime)


def next_prime(n: int) -> int:
    """
    Find the next prime number greater than n.

    :param n: The number to find the next prime of.
    :return: The next prime number after n.
    """
    next_number = n + 1
    while not is_prime(next_number):
        next_number += 1
    return next_number


def coprime(a: int, b: int) -> bool:
    """
    Determine if two numbers are coprime.

    :param a: The first number.
    :param b: The second number.
    :return: True if a and b are coprime, False otherwise.
    """
    while b:
        a, b = b, a % b
    return a == 1


def is_catalan_number(n: int) -> bool:
    """
    Check if a number is a Catalan number.

    The function checks if the given number is a Catalan number. Catalan numbers are a sequence of natural numbers
    that have applications in combinatorial mathematics, each number being the solution to a problem in combinatorial
    enumeration.

    :param n: The number to check.
    :return: True if n is a Catalan number, False otherwise.
    """
    catalan = 1
    i = 0
    while catalan < n:
        i += 1
        catalan = catalan * 2 * (2 * i - 1) / (i + 1)
    return catalan == n


def calculate_euler_phi(n: int) -> int:
    """
    Calculate the Euler's Totient Function φ(n).

    Euler's Totient Function φ(n) is an important function in number theory that counts the positive integers up to a
    given integer n that are relatively prime to n.

    :param n: The input number to calculate φ(n) for.
    :return: The value of φ(n).
    """
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result


def is_smooth_number(n: int, b: int) -> bool:
    """
    Check if a number is a b-smooth number.

    A b-smooth number is an integer that has no prime divisors greater than b. For example, a 7-smooth number is
    divisible by no primes greater than 7.

    :param n: The number to check.
    :param b: The smoothness bound.
    :return: True if n is a b-smooth number, False otherwise.
    """
    prime = 2
    while prime <= b and n > 1:
        if n % prime == 0:
            while n % prime == 0:
                n //= prime
        prime += 1
    return n == 1


def calculate_totient_sum(n: int) -> int:
    """
    Calculate the sum of Euler's Totient function φ(k) for all k from 1 to n.

    This function calculates the sum of the values of Euler's Totient function φ(k) for all integers k from 1 up to n.
    The Totient function is used in number theory to count the number of positive integers up to a given integer n
    that are relatively prime to n.

    :param n: The upper limit of the range to calculate the sum for.
    :return: The sum of φ(k) for all k from 1 to n.
    """
    sum_phi = 0
    for k in range(1, n + 1):
        sum_phi += calculate_euler_phi(k)
    return sum_phi


def is_fibonacci_number(n: int) -> bool:
    """
    Check if a number is a Fibonacci number.

    A Fibonacci number is a number that appears in the Fibonacci sequence, where each number is the sum of the two
    preceding ones, usually starting with 0 and 1.

    :param n: The number to check.
    :return: True if n is a Fibonacci number, False otherwise.
    """
    a, b = 0, 1
    while a < n:
        a, b = b, a + b
    return a == n


def calculate_totient(n: int) -> int:
    """
    Calculate Euler's Totient Function for a given number.

    :param n: The number to calculate the totient for
    :return: The value of Euler's Totient Function for n
    """
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result


def modular_inverse(a: int, m: int) -> int:
    """
    Calculate the modular multiplicative inverse of a under modulo m.

    :param a: The number to find the inverse of
    :param m: The modulo
    :return: The modular multiplicative inverse of a modulo m
    """
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def calculate_prime_gap(n: int) -> int:
    """
    Calculate the gap between a given prime number and the next prime number.

    :param n: The starting prime number to calculate the gap from.
    :return: The gap between the given prime number and the next prime number.
    """
    current = n + 1
    while not is_prime(current):
        current += 1
    return current - n


def calculate_carmichael_function(n: int) -> int:
    """
    Calculate the Carmichael function of a given number.

    :param n: The number to calculate the Carmichael function for.
    :return: The value of the Carmichael function for the given number.
    """

    def lcm(x: int, y: int) -> int:
        return x * y // gcd(x, y)

    if n == 1:
        return 1
    prime_factors_set = set(calculate_prime_factors(n))
    lcm_result = 1
    for prime in prime_factors_set:
        power = n
        while power % prime == 0:
            power //= prime
        if prime == 2 and n // (2 ** (calculate_prime_factors(n).count(2))) >= 4:
            lcm_result = lcm(
                lcm_result,
                (prime - 1) * (2 ** (calculate_prime_factors(n).count(2) - 2)),
            )
        else:
            lcm_result = lcm(lcm_result, prime - 1)
    return lcm_result


def calculate_legendre_symbol(a: int, p: int) -> int:
    """
    Calculate the Legendre symbol (a/p).

    :param a: The numerator of the Legendre symbol.
    :param p: The denominator of the Legendre symbol, which must be an odd prime.
    :return: The value of the Legendre symbol.
    """
    if a % p == 0:
        return 0
    elif pow(a, (p - 1) // 2, p) == 1:
        return 1
    else:
        return -1


def calculate_square(number: int) -> int:
    """
    Calculate the square of a given number.

    :param number: The number to be squared.
    :return: The square of the given number.
    """
    return number**2


def is_triangular_number(number: int) -> bool:
    """
    Determine if a given number is a triangular number.
    A triangular number is of the form n(n+1)/2 for some n.

    :param number: The number to check.
    :return: True if the number is triangular, False otherwise.
    """
    n = (-1 + (1 + 8 * number) ** 0.5) / 2
    return n.is_integer()


def calculate_digit_factorial_sum(number: int) -> int:
    """
    Calculate the sum of the factorials of each digit in a number.

    :param number: The number whose digit factorials are to be summed.
    :return: The sum of the factorials of the digits of the number.
    """

    def factorial(n: int) -> int:
        if n == 0:
            return 1
        else:
            return n * factorial(n - 1)

    return sum(factorial(int(digit)) for digit in str(number))


def is_pandigital(number: int) -> bool:
    """
    Determine if a number is pandigital, meaning it contains each digit from 1 to n exactly once.

    :param number: The number to check.
    :return: True if the number is pandigital, False otherwise.
    """
    number_str = str(number)
    digit_set = set(number_str)
    return (
        len(number_str) == len(digit_set)
        and "0" not in digit_set
        and all(str(digit) in digit_set for digit in range(1, len(number_str) + 1))
    )


def calculate_fermat_last_theorem(n: int, limit: int = 100) -> list:
    """
    Find solutions to Fermat's Last Theorem for a given n within a specified limit.
    Fermat's Last Theorem states that there are no three positive integers a, b, and c that satisfy
    the equation a^n + b^n = c^n for any integer value of n greater than 2.

    :param n: The exponent in Fermat's Last Theorem.
    :param limit: The upper limit for a, b, and c to be checked.
    :return: A list of tuples (a, b, c) that are solutions to the equation, if any.
    """
    solutions = []
    if n > 2:
        for a in range(1, limit):
            for b in range(a, limit):  # Start from a to avoid duplicate pairs
                c = (a**n + b**n) ** (1 / n)
                if c.is_integer() and c <= limit:
                    solutions.append((a, b, int(c)))
    return solutions


def euler_totient(n: int) -> int:
    """
    Calculate the Euler's Totient function of a number.

    :param n: The number to calculate the Euler's Totient for
    :return: The value of Euler's Totient function for n
    """
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result


def calculate_mobius(n: int) -> int:
    """
    Calculate the Möbius function for a given number.

    The Möbius function is defined as:
    0 if n has a squared prime factor,
    1 if n is a product of an even number of distinct prime factors,
    -1 if n is a product of an odd number of distinct prime factors.

    :param n: The number to calculate the Möbius function for
    :return: The value of the Möbius function for n
    """
    if n == 1:
        return 1
    prime_factors = set()
    for i in range(2, int(n**0.5) + 1):
        while n % i == 0:
            prime_factors.add(i)
            n //= i
            if n % i == 0:
                return 0
    if n > 1:
        prime_factors.add(n)
    return -1 if len(prime_factors) % 2 else 1


def modular_pow(base: int, exponent: int, modulus: int) -> int:
    """
    Calculate the modular exponentiation.

    :param base: The base number
    :param exponent: The exponent
    :param modulus: The modulus
    :return: The result of (base ** exponent) % modulus
    """
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result


def calculate_prime_density(n: int) -> float:
    """
    Calculate the prime density up to a given number n.

    The prime density is defined as the ratio of the number of prime numbers up to n
    to the total number of positive integers up to n.

    :param n: The upper limit to calculate the prime density for.
    :return: The prime density as a float.
    """
    prime_count = sum(is_prime(i) for i in range(2, n + 1))
    return prime_count / n if n > 0 else 0


def calculate_totient_ratio(n: int) -> float:
    """
    Calculate the ratio of Euler's totient function φ(n) to n.

    Euler's totient function φ(n) is the number of positive integers up to n that are
    relatively prime to n.

    :param n: The number to calculate the totient ratio for.
    :return: The totient ratio as a float.
    """
    if n < 1:
        return 0

    def gcd(a: int, b: int) -> int:
        """Compute the greatest common divisor of a and b."""
        while b:
            a, b = b, a % b
        return a

    totatives = sum(1 for i in range(1, n + 1) if gcd(i, n) == 1)
    return totatives / n


def is_smooth(n: int, b: int) -> bool:
    """
    Determine if a number is b-smooth.

    A number is b-smooth if its largest prime factor does not exceed b.

    :param n: The number to check for b-smoothness.
    :param b: The smoothness bound.
    :return: True if n is b-smooth, False otherwise.
    """
    if n < 2:
        return False
    return max(calculate_prime_factors(n)) <= b


def lcm(a: int, b: int) -> int:
    """
    Compute the least common multiple (LCM) of two numbers.

    :param a: First number
    :param b: Second number
    :return: The LCM of a and b
    """
    return abs(a * b) // gcd(a, b)


def sum_of_divisors(n: int) -> int:
    """
    Calculate the sum of all divisors of a number, including 1 and the number itself.

    :param n: The input number
    :return: The sum of all divisors of n
    """
    total = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            sum_ = 1
            term = 1
            while n % p == 0:
                n = n // p
                term = term * p
                sum_ += term
            total *= sum_
        p += 1
    if n > 1:
        total *= 1 + n
    return total


# geometry


def calculate_diagonal_of_square(side_length: float) -> float:
    """
    Calculate the length of the diagonal of a square.

    :param side_length: The length of one side of the square.
    :return: The length of the diagonal of the square.
    """
    return (2**0.5) * side_length


def calculate_surface_area_of_regular_octahedron(edge_length: float) -> float:
    """
    Calculate the surface area of a regular octahedron.

    :param edge_length: The length of an edge of the octahedron.
    :return: The surface area of the octahedron.
    """
    return 2 * (3**0.5) * edge_length**2


def calculate_edge_length_of_cube_from_volume(volume: float) -> float:
    """
    Calculate the edge length of a cube given its volume.

    :param volume: The volume of the cube.
    :return: The edge length of the cube.
    """
    return volume ** (1 / 3)


def calculate_perimeter_of_equilateral_triangle(side_length: float) -> float:
    """
    Calculate the perimeter of an equilateral triangle.

    :param side_length: The length of a side of the equilateral triangle.
    :return: The perimeter of the equilateral triangle.
    """
    return 3 * side_length


def calculate_diagonal_of_cube(side_length: float) -> float:
    """
    Calculate the length of the diagonal of a cube given its side length.

    :param side_length: The length of a side of the cube.
    :return: The length of the diagonal of the cube.
    """
    return side_length * (3**0.5)


def calculate_length_of_regular_polygon_side(perimeter: float, num_sides: int) -> float:
    """
    Calculate the length of a side of a regular polygon given its perimeter and the number of sides.

    :param perimeter: The perimeter of the polygon.
    :param num_sides: The number of sides of the polygon.
    :return: The length of a side of the polygon.
    """
    return perimeter / num_sides


def calculate_diagonal_of_cuboid(length: float, width: float, height: float) -> float:
    """
    Calculate the diagonal of a cuboid given its length, width, and height.

    :param length: The length of the cuboid.
    :param width: The width of the cuboid.
    :param height: The height of the cuboid.
    :return: The length of the diagonal of the cuboid.
    """
    return (length**2 + width**2 + height**2) ** 0.5


def calculate_length_of_arc(radius: float, angle: float) -> float:
    """
    Calculate the length of an arc of a circle given the radius and the central angle in radians.

    :param radius: The radius of the circle.
    :param angle: The central angle in radians.
    :return: The length of the arc.
    """
    return radius * angle


def calculate_equilateral_triangle_height(side_length: float) -> float:
    """
    Calculate the height of an equilateral triangle given the length of a side.

    :param side_length: The length of a side of the equilateral triangle.
    :return: The height of the equilateral triangle.
    """
    return (side_length * (3**0.5)) / 2


def calculate_diagonal_of_hexagon(side_length: float) -> float:
    """
    Calculate the diagonal length of a regular hexagon given its side length.

    :param side_length: The length of a side of the hexagon.
    :return: The length of the diagonal of the hexagon.
    """
    return 2 * side_length


def calculate_edge_length_of_octahedron_from_volume(volume: float) -> float:
    """
    Calculate the edge length of a regular octahedron given its volume.

    :param volume: The volume of the octahedron.
    :return: The edge length of the octahedron.
    """
    from math import sqrt

    return (2 * volume / (sqrt(2) / 3)) ** (1 / 3)


def calculate_inscribed_sphere_radius_in_tetrahedron(edge_length: float) -> float:
    """
    Calculate the radius of the inscribed sphere (incircle) in a regular tetrahedron given its edge length.

    :param edge_length: The length of an edge of the tetrahedron.
    :return: The radius of the inscribed sphere.
    """
    from math import sqrt

    return edge_length * sqrt(6) / 12


def calculate_diagonal_of_parallelepiped(
    length: float, width: float, height: float
) -> float:
    """
    Calculate the body diagonal of a parallelepiped given its dimensions.

    :param length: The length of the parallelepiped.
    :param width: The width of the parallelepiped.
    :param height: The height of the parallelepiped.
    :return: The length of the body diagonal of the parallelepiped.
    """
    return (length**2 + width**2 + height**2) ** 0.5


def calculate_spherical_wedge_volume(radius: float, angle: float) -> float:
    """
    Calculate the volume of a spherical wedge given the radius and angle in radians.

    :param radius: The radius of the sphere.
    :param angle: The angle at the apex of the wedge in radians.
    :return: The volume of the spherical wedge.
    """
    return (2 / 3) * (radius**3) * angle


def calculate_circular_ring_circumference(
    outer_radius: float, inner_radius: float
) -> float:
    """
    Calculate the circumference of a circular ring given the outer and inner radii.

    :param outer_radius: The outer radius of the ring.
    :param inner_radius: The inner radius of the ring.
    :return: The total circumference of the circular ring.
    """
    from math import pi

    return 2 * pi * (outer_radius + inner_radius)


def calculate_volume_of_cuboid(length: float, width: float, height: float) -> float:
    """
    Calculate the volume of a cuboid given its length, width, and height.

    :param length: The length of the cuboid.
    :param width: The width of the cuboid.
    :param height: The height of the cuboid.
    :return: The volume of the cuboid.
    """
    return length * width * height


def calculate_perimeter_of_circle(radius: float) -> float:
    """
    Calculate the perimeter (circumference) of a circle given its radius.

    :param radius: The radius of the circle
    :return: The perimeter of the circle
    """
    from math import pi

    return 2 * pi * radius


def calculate_edge_length_of_regular_octahedron_from_volume(volume: float) -> float:
    """
    Calculate the edge length of a regular octahedron given its volume.

    :param volume: The volume of the octahedron
    :return: The edge length of the octahedron
    """
    return (2 * (volume ** (1 / 3))) / (3**0.5)


def calculate_pyramid_surface_area(base_length: float, slant_height: float) -> float:
    """
    Calculate the surface area of a square-based pyramid.

    :param base_length: The length of the base edge of the pyramid.
    :param slant_height: The slant height of the pyramid.
    :return: The total surface area of the pyramid.
    """
    base_area = base_length**2
    lateral_area = 4 * (base_length * slant_height) / 2
    return base_area + lateral_area


def calculate_cylinder_lateral_surface_area(radius: float, height: float) -> float:
    """
    Calculate the lateral surface area of a cylinder.

    :param radius: The radius of the cylinder base.
    :param height: The height of the cylinder.
    :return: The lateral surface area of the cylinder.
    """
    from math import pi

    return 2 * pi * radius * height


def calculate_cone_surface_area(radius: float, slant_height: float) -> float:
    """
    Calculate the total surface area of a cone, including the base.

    :param radius: The radius of the cone's base.
    :param slant_height: The slant height of the cone.
    :return: The total surface area of the cone.
    """
    from math import pi

    base_area = pi * radius**2
    lateral_area = pi * radius * slant_height
    return base_area + lateral_area


def calculate_prism_volume(base_area: float, height: float) -> float:
    """
    Calculate the volume of a prism.

    :param base_area: The area of the prism's base.
    :param height: The height of the prism.
    :return: The volume of the prism.
    """
    return base_area * height


def calculate_volume_of_regular_tetrahedron(edge_length: float) -> float:
    """
    Calculate the volume of a regular tetrahedron given its edge length.

    :param edge_length: The length of an edge of the tetrahedron
    :return: The volume of the tetrahedron
    """
    return (edge_length**3) / (6 * (2**0.5))


def calculate_equilateral_triangle_area(side_length: float) -> float:
    """
    Calculate the area of an equilateral triangle given the length of a side.

    :param side_length: The length of one side of the equilateral triangle
    :return: The area of the equilateral triangle
    """
    return (3**0.5 / 4) * side_length**2


def calculate_pyramid_volume(base_area: float, height: float) -> float:
    """
    Calculate the volume of a pyramid given the base area and height.

    :param base_area: The area of the base of the pyramid
    :param height: The height of the pyramid from the base to the apex
    :return: The volume of the pyramid
    """
    return (base_area * height) / 3


def calculate_cylinder_volume(radius: float, height: float) -> float:
    """
    Calculate the volume of a right circular cylinder given the radius and height.

    :param radius: The radius of the base of the cylinder
    :param height: The height of the cylinder
    :return: The volume of the cylinder
    """
    from math import pi

    return pi * (radius**2) * height


def calculate_cone_volume(radius: float, height: float) -> float:
    """
    Calculate the volume of a right circular cone given the radius of the base and height.

    :param radius: The radius of the base of the cone
    :param height: The height of the cone
    :return: The volume of the cone
    """
    from math import pi

    return (pi * (radius**2) * height) / 3


def calculate_diagonal_of_polygon(side_length: float, number_of_sides: int) -> float:
    """
    Calculate the length of the diagonal of a regular polygon.

    :param side_length: The length of one side of the polygon.
    :param number_of_sides: The total number of sides (or vertices) of the polygon.
    :return: The length of the diagonal of the polygon.
    """
    from math import pi, tan

    return 2 * side_length * tan(pi / number_of_sides)


def calculate_parallelogram_perimeter(base_length: float, side_length: float) -> float:
    """
    Calculate the perimeter of a parallelogram.

    :param base_length: The length of the base of the parallelogram.
    :param side_length: The length of the side of the parallelogram.
    :return: The perimeter of the parallelogram.
    """
    return 2 * (base_length + side_length)


def calculate_ellipse_perimeter(
    semi_major_axis: float, semi_minor_axis: float
) -> float:
    """
    Calculate the approximate perimeter of an ellipse.

    :param semi_major_axis: The length of the semi-major axis of the ellipse.
    :param semi_minor_axis: The length of the semi-minor axis of the ellipse.
    :return: The approximate perimeter of the ellipse.
    """
    from math import pi, sqrt

    return 2 * pi * sqrt((semi_major_axis**2 + semi_minor_axis**2) / 2)


def calculate_circle_radius_inscribed_in_rectangle(
    length: float, width: float
) -> float:
    """
    Calculate the radius of the inscribed circle in a rectangle.

    :param length: The length of the rectangle.
    :param width: The width of the rectangle.
    :return: The radius of the inscribed circle.
    """
    # The radius of the inscribed circle is half the length of the shorter side of the rectangle.
    return min(length, width) / 2


def calculate_diagonal_of_regular_tetrahedron(edge_length: float) -> float:
    """
    Calculate the diagonal of a regular tetrahedron.

    :param edge_length: The length of an edge of the tetrahedron.
    :return: The length of the diagonal of the tetrahedron.
    """
    return edge_length * (2**0.5)


def calculate_volume_of_regular_dipyramid(edge_length: float, height: float) -> float:
    """
    Calculate the volume of a regular dipyramid.

    :param edge_length: The length of the base edge of the dipyramid.
    :param height: The height of the dipyramid from the base to the apex.
    :return: The volume of the dipyramid.
    """
    base_area = (3**0.5 / 4) * edge_length**2
    return 1 / 3 * base_area * height


def calculate_parallelogram_area(base: float, height: float) -> float:
    """
    Calculate the area of a parallelogram.

    :param base: The length of the base of the parallelogram.
    :param height: The height of the parallelogram.
    :return: The area of the parallelogram.
    """
    return base * height


def calculate_ellipse_area(semi_major_axis: float, semi_minor_axis: float) -> float:
    """
    Calculate the area of an ellipse given its semi-major and semi-minor axes.

    :param semi_major_axis: The length of the semi-major axis of the ellipse
    :param semi_minor_axis: The length of the semi-minor axis of the ellipse
    :return: The area of the ellipse
    """
    from math import pi

    return pi * semi_major_axis * semi_minor_axis


def calculate_surface_area_of_cube(edge_length: float) -> float:
    """
    Calculate the surface area of a cube.

    :param edge_length: The length of an edge of the cube.
    :return: The surface area of the cube.
    """
    return 6 * (edge_length**2)


def calculate_distance_between_points(
    x1: float, y1: float, x2: float, y2: float
) -> float:
    """
    Calculate the distance between two points in a 2D plane.

    :param x1: x-coordinate of the first point
    :param y1: y-coordinate of the first point
    :param x2: x-coordinate of the second point
    :param y2: y-coordinate of the second point
    :return: The distance between the two points
    """
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def calculate_spherical_surface_area(radius: float) -> float:
    """
    Calculate the surface area of a sphere given its radius.

    :param radius: The radius of the sphere
    :return: The surface area of the sphere
    """
    from math import pi

    return 4 * pi * radius**2


def calculate_cylinder_lateral_area(radius: float, height: float) -> float:
    """
    Calculate the lateral surface area of a cylinder given its radius and height.

    :param radius: The radius of the cylinder's base
    :param height: The height of the cylinder
    :return: The lateral surface area of the cylinder
    """
    from math import pi

    return 2 * pi * radius * height


# topology


def calculate_betti_number_for_torus(torus_dimension: int) -> int:
    """
    Calculate the Betti number for a torus of a given dimension.

    The Betti number in this context refers to the rank of the homology group,
    which, for a torus, equals 2 * dimension of the torus.

    :param torus_dimension: The dimension of the torus.
    :return: The Betti number for the torus.
    """
    return 2 * torus_dimension


def calculate_euler_characteristic_by_type(surface_type: str) -> int:
    """
    Calculate the Euler characteristic for a given surface type.

    The Euler characteristic is a topological invariant that describes the shape
    of a topological space regardless of the way it is bent, stretched, or compressed.

    :param surface_type: The type of surface ('sphere', 'torus', or 'projective_plane').
    :return: The Euler characteristic of the surface.
    """
    if surface_type == "sphere":
        return 2
    elif surface_type == "torus":
        return 0
    elif surface_type == "projective_plane":
        return 1
    else:
        raise ValueError("Invalid surface type")


def calculate_genus_of_surface(euler_characteristic: int) -> int:
    """
    Calculate the genus of a closed orientable surface based on its Euler characteristic.

    The genus of a surface is a measure of the maximum number of non-intersecting simple
    closed curves that can be drawn on the surface without separating it.

    :param euler_characteristic: The Euler characteristic of the surface.
    :return: The genus of the surface.
    """
    return (2 - euler_characteristic) // 2


def calculate_fundamental_group_of_circle() -> str:
    """
    Calculate the fundamental group of the circle.

    The fundamental group of the circle, denoted as π1(S^1), is isomorphic to the integers (Z),
    representing the winding number around the circle.

    :return: A string representation of the fundamental group of the circle.
    """
    return "Z"


def calculate_fixed_point(
    f, initial_guess: float, tolerance: float = 1e-5, max_iterations: int = 1000
) -> float:
    """
    Calculate the fixed point of a function, where f(x) = x.

    :param f: A function for which the fixed point is to be found.
    :param initial_guess: The initial guess for the fixed point.
    :param tolerance: The tolerance for the difference between successive approximations.
    :param max_iterations: The maximum number of iterations to perform.
    :return: The approximated fixed point of the function.
    """
    x0 = initial_guess
    for _ in range(max_iterations):
        x1 = f(x0)
        if abs(x1 - x0) < tolerance:
            return x1
        x0 = x1
    return x0


def calculate_klein_bottle_area(radius: float) -> float:
    """
    Calculate the surface area of a Klein bottle.
    The Klein bottle is a non-orientable surface, and its "surface area" in the traditional sense is not well-defined.
    However, for the purpose of this function, we'll use a hypothetical formula for educational purposes.

    :param radius: The radius of the Klein bottle.
    :return: The surface area of the Klein bottle.
    """
    from math import pi

    return 4 * pi * radius**2


def calculate_alexander_polynomial(knot: str) -> str:
    """
    Calculate the Alexander polynomial of a knot given its notation.

    :param knot: The notation of the knot (e.g., "3_1" for the trefoil knot).
    :return: The Alexander polynomial of the knot as a string.
    """
    # This is a placeholder function. In practice, calculating the Alexander polynomial
    # requires more complex algebraic topology concepts not easily implemented in a short function.
    # Here, we return a simple example for educational purposes.
    if knot == "3_1":  # Trefoil knot
        return "t^2 - t + 1"
    else:
        return "1"


def calculate_homology_group(rank: int) -> str:
    """
    Calculate the homology group of a topological space based on its rank.

    :param rank: The rank of the homology group, typically denoted as an integer.
    :return: A string representation of the homology group, assuming it's a finitely generated abelian group.

    The rank of the homology group is a fundamental concept in algebraic topology, representing the number of
    "holes" of a given dimension in a topological space. This function simplifies the concept by returning a
    string representation of the homology group based on its rank.
    """
    if rank == 0:
        return "Z"
    elif rank > 0:
        return f"Z^{rank}"
    else:
        return "Invalid rank"


def calculate_euler_characteristic(vertices: int, edges: int, faces: int) -> int:
    """
    Calculate the Euler characteristic of a polyhedron.

    :param vertices: The number of vertices in the polyhedron.
    :param edges: The number of edges in the polyhedron.
    :param faces: The number of faces in the polyhedron.
    :return: The Euler characteristic of the polyhedron.

    The Euler characteristic is a topological invariant, a number that describes a topological space's
    shape or structure regardless of the way it is bent. It is calculated for a polyhedron by subtracting
    the number of edges from the sum of the number of vertices and faces.
    """
    return vertices - edges + faces


def calculate_fundamental_group_of_torus() -> str:
    """
    Calculate the fundamental group of a torus.

    :return: A string representation of the fundamental group of a torus.

    The fundamental group of a torus is an important concept in algebraic topology, representing the set of
    all loops on a torus up to continuous deformation. For a torus, this group is represented by Z x Z,
    indicating two independent loops around the torus's major and minor circumferences.
    """
    return "Z x Z"


def calculate_covering_space_number(base_space: str) -> int | float:
    """
    Calculate the number of covering spaces for a given base space.

    In topology, a covering space is a space that "covers" another space (the base space) in a specific
    way. The number of covering spaces can vary significantly depending on the base space. This function
    simplifies the concept by providing predefined outcomes for a circle and a torus.

    :param base_space: The name of the base space, expected to be either "circle" or "torus".
    :return: The number of covering spaces for the given base space.
    """
    if base_space == "circle":
        return float("inf")  # Infinite number of covering spaces for a circle
    elif base_space == "torus":
        return float("inf")  # Infinite number of covering spaces for a torus
    else:
        return 0  # Undefined or no covering spaces for other base spaces


def calculate_borsuk_ulam_theorem_points(sphere_dimension: int) -> str:
    """
    Apply the Borsuk-Ulam theorem to find the number of points with matching conditions.

    :param sphere_dimension: The dimension of the sphere to apply the Borsuk-Ulam theorem.
    :return: A string indicating the outcome of applying the Borsuk-Ulam theorem.

    The Borsuk-Ulam theorem states that for any continuous function from an n-dimensional sphere to
    Euclidean n-space, there exists a pair of antipodal points on the sphere that are mapped to the same
    point in Euclidean space. This function returns a simplified interpretation of the theorem's implications.
    """
    if sphere_dimension >= 0:
        return "At least one pair of antipodal points maps to the same point."
    else:
        return "Invalid dimension"


def calculate_homotopy_group_sphere(n: int) -> str:
    """
    Calculate the n-th homotopy group of a sphere.

    :param n: The dimension of the homotopy group.
    :return: A string representation of the n-th homotopy group of a sphere.

    The homotopy groups of spheres are fundamental objects in algebraic topology.
    For n=0, the group is trivial. For n=1, it is isomorphic to the integers.
    For n=2, it is also isomorphic to the integers. For n>2, the groups are more complex
    and are generally not fully known or are infinite.
    """
    if n == 0:
        return "Trivial group"
    elif n == 1 or n == 2:
        return "Z (the integers)"
    else:
        return "Complex or unknown structure"


def calculate_knot_group(knot: str) -> str:
    """
    Calculate the fundamental group of a knot.

    The fundamental group of a knot, also known as the knot group, is an important
    invariant in knot theory, a branch of topology. It gives insight into the
    topological properties of the knot.

    :param knot: The name or type of the knot.
    :return: A string representation of the fundamental group of the knot.
    """
    if knot.lower() == "unknot":
        return "Trivial group"
    elif knot.lower() == "trefoil":
        return "<a, b | a^3 = b^2>"
    elif knot.lower() == "figure-eight":
        return "<a, b | abab^-1a^-1b^-1 = 1>"
    else:
        return "Unknown or complex structure"


def calculate_euler_poincare_characteristic(space: str) -> int:
    """
    Calculate the Euler-Poincaré characteristic of a given topological space.

    :param space: The name or type of the topological space.
    :return: An integer representing the Euler-Poincaré characteristic of the space.

    The Euler-Poincaré characteristic is a topological invariant, a number that describes
    a topological space's shape or structure regardless of the way it is bent.
    """
    if space.lower() == "sphere":
        return 2
    elif space.lower() == "torus":
        return 0
    elif space.lower() == "projective plane":
        return 1
    else:
        return -1  # Indicates an unknown or not applicable characteristic


def calculate_genus_of_orientable_surface(euler_char: int) -> int:
    """
    Calculate the genus of an orientable surface based on its Euler characteristic.

    :param euler_char: The Euler characteristic of the surface.
    :return: An integer representing the genus of the surface.

    The genus of an orientable surface is a measure of the maximum number of non-intersecting
    simple closed curves that can be drawn on the surface without separating it.
    """
    return (2 - euler_char) // 2


def calculate_mobius_band_length(width: float, radius: float) -> float:
    """
    Calculate the length of the central circle of a Möbius band.

    :param width: The width of the Möbius band.
    :param radius: The radius from the center of the Möbius strip to the middle of the band.
    :return: The length of the central circle of the Möbius band as a float.

    The function calculates the length of the central circle of a Möbius band, which is simply the circumference
    of a circle with the given radius.
    """
    from math import pi

    return 2 * pi * radius


def calculate_mobius_inversion(u: int) -> int:
    """
    Calculate the value of the Möbius function for a given integer.

    :param u: The integer for which the Möbius function value is to be calculated.
    :return: The value of the Möbius function for the given integer.
    """
    if u == 1:
        return 1
    p = 0
    for i in range(2, int(u**0.5) + 1):
        if u % i == 0:
            if u % (i * i) == 0:
                return 0
            else:
                p += 1
    return -1 if p % 2 else 1


def calculate_genus_of_graph(edges: int, vertices: int) -> int:
    """
    Calculate the genus of a graph given its edges and vertices.

    :param edges: The number of edges in the graph.
    :param vertices: The number of vertices in the graph.
    :return: The genus of the graph.
    """
    return (edges - vertices - (2 - 2 * 1)) // 2


def calculate_kirchhoff_index(graph: list[list[int]]) -> float:
    """
    Calculate the Kirchhoff index of a graph.

    :param graph: A square adjacency matrix representing the graph, where graph[i][j] is 1 if
        there is an edge between vertices i and j, and 0 otherwise.
    :return: The Kirchhoff index of the graph.
    """
    import numpy as np

    n = len(graph)
    L = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                L[i][j] = sum(graph[i])
            elif graph[i][j]:
                L[i][j] = -1
    L_inv = np.linalg.pinv(L)
    return np.sum(L_inv)


def calculate_genus(euler_characteristic: int) -> int:
    """
    Calculate the genus of a closed orientable surface.

    :param euler_characteristic: The Euler characteristic of the surface.
    :return: The genus of the surface.

    The genus is a topological property that represents the maximum number of non-intersecting simple closed
    curves that can be drawn on the surface without separating it.
    """
    return (2 - euler_characteristic) // 2


def calculate_betti_number(euler_characteristic: int, dimension: int) -> int:
    """
    Calculate the Betti number of a topological space.

    :param euler_characteristic: The Euler characteristic of the space.
    :param dimension: The dimension for which to calculate the Betti number.
    :return: The Betti number for the given dimension.

    The Betti numbers are topological invariants that generalize the notion of connectivity.
    """
    if dimension == 0:
        return 1  # Simplified assumption for connected spaces
    elif dimension == 1:
        return euler_characteristic - 1
    else:
        return 0  # Simplified for higher dimensions without specific topology


def calculate_covering_space_degree(
    base_space_genus: int, covering_space_genus: int
) -> int:
    """
    Calculate the degree of a covering map between two surfaces based on their genus.

    :param base_space_genus: The genus of the base space.
    :param covering_space_genus: The genus of the covering space.
    :return: The degree of the covering map.

    The degree of a covering map is the number of times the covering space covers the base space.
    """
    if base_space_genus == 0:
        return 0 if covering_space_genus == 0 else covering_space_genus + 1
    else:
        return (covering_space_genus - 1) // (base_space_genus - 1)


def calculate_homotopy_classes(S: int, X: int) -> int:
    """
    Calculate the number of homotopy classes of maps from a sphere S^n to a space X.

    This function is a simplification and does not reflect actual topological complexity.

    :param S: The dimension of the sphere S^n.
    :param X: The homotopy dimension of the space X.
    :return: The number of homotopy classes of maps from S^n to X.
    """
    return S * X + 1


def calculate_wedge_sum_euler_characteristic(components: list[int]) -> int:
    """
    Calculate the Euler characteristic of a wedge sum of spaces given their Euler characteristics.

    The Euler characteristic of a wedge sum is the sum of the Euler characteristics
    of its components minus the number of components minus 1.

    :param components: A list of Euler characteristics of the components.
    :return: The Euler characteristic of the wedge sum.
    """
    return sum(components) - len(components) + 1


def calculate_fiber_bundle_euler_characteristic(base: int, fiber: int) -> int:
    """
    Calculate the Euler characteristic of a fiber bundle given the Euler characteristics of the base and the fiber.

    Assumes the fiber bundle is orientable and the base and fiber are connected.

    :param base: The Euler characteristic of the base space.
    :param fiber: The Euler characteristic of the fiber space.
    :return: The Euler characteristic of the fiber bundle.
    """
    return base * fiber


def calculate_covering_space_euler_characteristic(base: int, sheets: int) -> int:
    """
    Calculate the Euler characteristic of a covering space.

    The Euler characteristic of a covering space is the product of the Euler characteristic
    of the base space and the number of sheets.

    :param base: The Euler characteristic of the base space.
    :param sheets: The number of sheets in the covering space.
    :return: The Euler characteristic of the covering space.
    """
    return base * sheets


def calculate_product_space_euler_characteristic(space1: int, space2: int) -> int:
    """
    Calculate the Euler characteristic of a product space given the Euler characteristics of the two spaces.

    The Euler characteristic of a product space is the product of the Euler characteristics of the two spaces.

    :param space1: The Euler characteristic of the first space.
    :param space2: The Euler characteristic of the second space.
    :return: The Euler characteristic of the product space.
    """
    return space1 * space2


def calculate_homotopy_type_euler_characteristic(
    vertices: int, edges: int, faces: int
) -> int:
    """
    Calculate the Euler characteristic of a homotopy type based on its vertices, edges, and faces.

    The Euler characteristic is a topological invariant that is calculated as χ = V - E + F,
    where V is the number of vertices, E is the number of edges, and F is the number of faces.

    :param vertices: The number of vertices in the homotopy type.
    :param edges: The number of edges in the homotopy type.
    :param faces: The number of faces in the homotopy type.
    :return: The Euler characteristic of the homotopy type.
    """
    return vertices - edges + faces


def calculate_knot_complement_volume(knot_type: str) -> float:
    """
    Estimate the volume of the complement of a knot in S^3, given its type.

    Note: In practice, the volume of a knot complement is determined through more complex
    geometric and topological analysis. This function provides simplified, illustrative
    estimates for common knots.

    :param knot_type: A string representing the type of the knot (e.g., "trefoil", "figure-eight").
    :return: An estimated volume of the knot complement. This function returns a fixed
             value based on common knot types for demonstration purposes.
    """
    knot_volumes = {"trefoil": 2.029883, "figure-eight": 2.828122}
    return knot_volumes.get(knot_type, 0.0)


def calculate_covering_space_lifts(base_space: str, covering_space: str) -> int:
    """
    Estimate the number of lifts in a covering space given the base space and the covering space.

    :param base_space: A string representing the type of the base space (e.g., "circle", "torus").
    :param covering_space: A string representing the type of the covering space (e.g., "cylinder", "double-torus").
    :return: An estimated number of lifts in the covering space. This function returns a fixed
             value based on common base and covering space combinations for demonstration purposes.

    Note: The actual calculation of lifts in a covering space involves detailed topological analysis.
    This function provides simplified, illustrative estimates for common scenarios.
    """
    lifts = {("circle", "cylinder"): 1, ("torus", "double-torus"): 2}
    return lifts.get((base_space, covering_space), 0)


def calculate_wedge_product_dimension(spaces: list[int]) -> int:
    """
    Calculate the dimension of the wedge product of a list of topological spaces.

    The dimension of the wedge product of a collection of spaces is the sum of the dimensions
    of those spaces. This function calculates that sum.

    :param spaces: A list of integers representing the dimensions of the topological spaces.
    :return: The dimension of the wedge product of the given spaces.
    """
    return sum(spaces)


def calculate_knot_invariant(knot_type: str) -> int:
    """
    Calculate a simplified invariant for a given knot type.

    Knot invariants are mathematical objects that allow distinguishing between different knots.
    This function provides a simplified calculation of a knot invariant based on the knot type.
    - For the "unknot", which is a simple loop, the invariant is 0.
    - For "trefoil", a common type of knot, the invariant is 3.
    - For "figure-eight", another common knot, the invariant is 4.
    - For other types of knots, the function returns -1, indicating an unknown or complex knot type.

    :param knot_type: A string representing the type of the knot.
    :return: An integer representing a simplified invariant of the knot.
    """
    if knot_type == "unknot":
        return 0
    elif knot_type == "trefoil":
        return 3
    elif knot_type == "figure-eight":
        return 4
    else:
        return -1


def calculate_borsuk_ulam_antipodal_points(n: int) -> str:
    """
    Determine if there exists a pair of antipodal points on the surface of an n-dimensional sphere
    that map to the same point in n-dimensional space.

    The Borsuk-Ulam theorem states that for any continuous function from an n-dimensional sphere to n-dimensional
    Euclidean space, there exists a pair of antipodal points on the sphere that map to the same point in space.
    This function returns a simplified explanation based on the dimension of the sphere.

    :param n: The dimension of the sphere.
    :return: A string indicating whether such a pair of points exists.
    """
    if n >= 1:
        return "Exists"
    else:
        return "Invalid dimension"


def calculate_genus_of_connected_sum(g1: int, g2: int) -> int:
    """
    Calculate the genus of the connected sum of two surfaces.

    In topology, the connected sum of two surfaces is a way of combining them into a new surface.
    The genus of the connected sum of two surfaces is the sum of their genera. This operation is
    fundamental in the classification of surfaces.

    :param g1: The genus of the first surface.
    :param g2: The genus of the second surface.
    :return: The genus of the connected sum of the two surfaces.
    """
    return g1 + g2


def calculate_homotopy_equivalence_spaces(n: int) -> int:
    """
    Calculate the number of homotopy equivalence classes for a given number of spaces.

    :param n: The number of topological spaces.
    :return: The number of homotopy equivalence classes.
    """
    return 2**n


def calculate_winding_number(path: list[list[float]], point: list[float]) -> int:
    """
    Calculate the winding number of a closed path around a given point.

    :param path: A list of tuples representing the points in the closed path.
    :param point: A tuple representing the point to calculate the winding number around.
    :return: The winding number.
    """
    winding_number = 0
    for i in range(len(path)):
        p1, p2 = path[i], path[(i + 1) % len(path)]
        if p1[1] <= point[1] < p2[1] or p2[1] <= point[1] < p1[1]:
            if (p2[0] - p1[0]) * (point[1] - p1[1]) > (point[0] - p1[0]) * (
                p2[1] - p1[1]
            ):
                winding_number += 1 if p1[1] <= point[1] else -1
    return winding_number


def calculate_fundamental_group_free_product(rank: int) -> str:
    """
    Calculate the fundamental group of a bouquet of circles, which is a free group.

    :param rank: The number of circles in the bouquet, representing the rank of the free group.
    :return: The presentation of the fundamental group as a string.
    """
    return f"F_{rank}"


def calculate_mobius_strip_area(length: float, width: float) -> float:
    """
    Calculate the surface area of a Möbius strip given its length and width.

    Note: The formula for the surface area of a Möbius strip is A = L * W.

    :param length: The length of the midline of the Möbius strip.
    :param width: The width of the strip.
    :return: The surface area of the Möbius strip.
    """
    return length * width


def calculate_trefoil_knot_length(radius: float) -> float:
    """
    Calculate the approximate length of a trefoil knot given the radius of its torus.

    Note: This function uses an approximation formula for simplicity.

    :param radius: The radius of the torus on which the trefoil knot lies.
    :return: The approximate length of the trefoil knot.
    """
    from math import pi

    return 2 * pi * radius * 2


def calculate_klein_bottle_volume(inner_radius: float) -> float:
    """
    Calculate the "volume" of a Klein bottle given the inner radius.

    Note: This function returns 0 as a conceptual representation of the Klein bottle's volume.

    :param inner_radius: The inner radius of the Klein bottle.
    :return: The "volume" of the Klein bottle, which is theoretically zero since it's a non-orientable surface.
    """
    return 0.0


def calculate_projective_plane_area(radius: float) -> float:
    """
    Calculate the area of a projective plane embedded in three dimensions given its radius.
    Note: This function uses a simplified formula for demonstration purposes.

    :param radius: The radius of the projective plane.
    :return: The area of the projective plane.
    """
    from math import pi

    return 2 * pi * radius**2


def calculate_torus_knot_complexity(p: int, q: int) -> int:
    """
    Calculate the complexity (minimum crossing number) of a (p, q)-torus knot.
    Note: The formula for the complexity of a (p, q)-torus knot is gcd(p, q) * (min(p, q) - 1).

    :param p: The first parameter of the torus knot, representing the number of times
        it wraps around the axis of symmetry.
    :param q: The second parameter of the torus knot, representing the number of times
        it wraps around a circle in the interior of the torus.
    :return: The minimum crossing number of the torus knot.
    """
    from math import gcd

    return gcd(p, q) * (min(p, q) - 1)


def calculate_homotopy_group_of_klein_bottle(n: int) -> str:
    """
    Calculate the n-th homotopy group of the Klein bottle.

    The Klein bottle is a non-orientable surface, which has interesting homotopy groups.
    For n=1, the fundamental group is non-abelian and is represented as a string for simplicity.
    For n>1, the homotopy groups are isomorphic to those of the 2-sphere.

    :param n: The homotopy group order
    :return: The n-th homotopy group of the Klein bottle as a string
    """
    if n == 1:
        return "Z + Z_2"
    elif n == 2:
        return "0"
    else:
        return "Z" if n % 2 == 0 else "0"


def calculate_covering_space_degree_of_torus(k: int) -> int:
    """
    Calculate the degree of a k-sheeted covering space of the torus.

    The degree of a covering space of the torus corresponds to the number of times
    the covering space wraps around the torus.

    :param k: The number of sheets in the covering space
    :return: The degree of the covering space
    """
    return k


def calculate_euler_characteristic_of_projective_plane() -> int:
    """
    Calculate the Euler characteristic of the real projective plane.

    The real projective plane is a non-orientable surface obtained by identifying opposite edges of a rectangle.
    Its Euler characteristic is a topological invariant.

    :return: The Euler characteristic of the real projective plane
    """
    return 1


def calculate_fundamental_group_of_klein_bottle() -> str:
    """
    Calculate the fundamental group of the Klein bottle.

    The fundamental group of the Klein bottle is non-abelian and is represented as a string for simplicity.
    It is generated by two elements a and b with the relation a^2 = b^2.

    :return: The fundamental group of the Klein bottle as a string
    """
    return "<a, b | a^2 = b^2>"


def calculate_genus_of_orientable_double_cover(k: int) -> int:
    """
    Calculate the genus of the orientable double cover of a non-orientable surface with k cross-caps.

    The genus of the orientable double cover of a non-orientable surface can be calculated
    based on the number of cross-caps.

    :param k: The number of cross-caps on the non-orientable surface
    :return: The genus of the orientable double cover
    """
    return k - 1


def calculate_homotopy_group_of_sphere(n: int) -> str:
    """
    Calculate the homotopy group of an n-sphere.

    The homotopy group of a sphere is a fundamental concept in algebraic topology,
    which describes the algebraic structure of continuous deformations (homotopies)
    of maps from an n-dimensional sphere into itself.

    :param n: Dimension of the sphere
    :return: Description of the homotopy group
    """
    if n == 0:
        return "Trivial group"
    elif n == 1:
        return "Infinite cyclic group (Z)"
    elif n == 2:
        return "Trivial group"
    elif n == 3:
        return "Infinite cyclic group (Z)"
    else:
        return "Complex structure, specific results known for particular n"


def calculate_covering_space_degree_of_circle(n: int) -> int:
    """
    Calculate the degree of the covering space of a circle by itself.

    The degree of a covering space is a fundamental concept in topology, representing
    the number of times a space covers another space. For circles, this is directly
    related to the number of times one circle wraps around another.

    :param n: Number of times the circle covers itself
    :return: Degree of the covering space
    """
    return n


def calculate_trefoil_knot_group() -> str:
    """
    Calculate the group of the trefoil knot.

    The group of a trefoil knot, also known as its fundamental group, is a key concept in knot theory,
    a branch of topology. It provides algebraic information about the knot.

    :return: Description of the group of the trefoil knot
    """
    return "Non-abelian group with presentation <x, y | x^2 = y^3>"


def calculate_projective_plane_euler_characteristic() -> int:
    """
    Calculate the Euler characteristic of the projective plane.

    The projective plane is a fundamental example in topology of a non-orientable surface.
    Its Euler characteristic is a key invariant in understanding its topological properties.

    :return: Euler characteristic of the projective plane
    """
    return 1


def calculate_knot_genus(knot_type: str) -> int:
    """
    Calculate the genus of a given knot type.

    The genus of a knot is an integer that represents a topological property of the knot.
    It is defined as the minimum genus of all Seifert surfaces for the knot. This function
    provides a simplified calculation based on common knot types.

    :param knot_type: Type of the knot as a string
    :return: Genus of the knot
    """
    if knot_type == "unknot":
        return 0
    elif knot_type == "trefoil":
        return 1
    elif knot_type == "figure-eight":
        return 1
    else:
        return -1  # Indicates unknown or more complex knot type


def calculate_covering_space_degree_by_names(
    base_space: str, covering_space: str
) -> int:
    """
    Calculate the degree of a covering space over a given base space.

    The degree of a covering space is the number of times the covering space
    covers the base space. This function provides a simplified calculation for
    common base and covering spaces in topology.

    :param base_space: The base space of the covering
    :param covering_space: The covering space
    :return: Degree of the covering space
    """
    if base_space == "circle" and covering_space == "circle":
        return 2  # Example: double cover
    elif base_space == "torus" and covering_space == "torus":
        return 4  # Example: quadruple cover
    else:
        return -1  # Indicates unknown or more complex cases


def calculate_betti_number_for_topological_space(topological_space: str, n: int) -> int:
    """
    Calculate the nth Betti number of a given topological space.
    Betti numbers are topological invariants that count the maximum number of cuts
    that can be made without dividing the space into two pieces, related to the
    dimension specified. This function provides simplified calculations for common
    topological spaces.

    :param topological_space: The topological space under consideration
    :param n: The dimension for which to calculate the Betti number
    :return: The nth Betti number of the topological space
    """
    if topological_space == "sphere" and n == 0:
        return 1
    elif topological_space == "torus" and n == 1:
        return 2
    elif topological_space == "klein bottle" and n == 1:
        return 1
    else:
        return 0  # Default case for higher dimensions or unknown spaces


def calculate_covering_space_degree_of_sphere(n: int) -> int:
    """
    Calculate the degree of the covering space of an n-sphere.

    This function calculates the degree of the universal covering space of an n-sphere.
    For n=1, the degree is infinite (represented by -1), otherwise, it is 2 for n>1.

    :param n: Dimension of the sphere
    :return: Degree of the covering space
    """
    if n == 1:
        return -1  # Infinite
    else:
        return 2


def calculate_fundamental_group_of_projective_plane() -> str:
    """
    Calculate the fundamental group of the real projective plane.

    This function returns a string describing the fundamental group of the real projective plane,
    which is Z/2Z, the cyclic group of order 2.

    :return: Description of the fundamental group
    """
    return "Z/2Z"


def calculate_euler_characteristic_of_torus(g: int) -> int:
    """
    Calculate the Euler characteristic of a genus-g torus.

    This function calculates the Euler characteristic of a torus based on its genus.
    The formula used is 2 - 2g.

    :param g: Genus of the torus
    :return: Euler characteristic of the torus
    """
    return 2 - 2 * g


def calculate_klein_bottle_fundamental_group() -> str:
    """
    Calculate the fundamental group of the Klein bottle.

    This function returns a string describing the fundamental group of the Klein bottle,
    which is a non-abelian group generated by two elements a and b with the relation abab^-1.

    :return: Description of the fundamental group
    """
    return "Generated by {a, b | abab^-1}"


def calculate_mobius_band_characteristic() -> int:
    """
    Calculate the Euler characteristic of a Möbius band.

    The Möbius band is a non-orientable surface with only one side and only one boundary component.
    The Euler characteristic of a Möbius band is a topological invariant that is fixed for all
    Möbius bands.

    :return: Euler characteristic of the Möbius band
    """
    return 0


def calculate_knot_complement_euler_characteristic(genus: int) -> int:
    """
    Calculate the Euler characteristic of a knot complement based on its genus.

    The Euler characteristic of a knot complement in S^3 can be calculated using the formula: χ = 2 - 2g,
    where g is the genus of the knot.

    :param genus: Genus of the knot
    :return: Euler characteristic of the knot complement
    """
    return 2 - 2 * genus


def calculate_torus_homology_group(dimension: int) -> str:
    """
    Calculate the homology group of a torus in a given dimension.

    Homology groups are algebraic structures that are used in algebraic topology to
    study topological spaces. The torus, being a product of two circles, has
    interesting homology groups that reflect its topological properties.

    :param dimension: Dimension of the homology group
    :return: Description of the homology group of the torus in the given dimension
    """
    if dimension == 0:
        return "Z"
    elif dimension == 1:
        return "Z ⊕ Z"
    elif dimension == 2:
        return "Z"
    else:
        return "Trivial group"


def calculate_fixed_point_iteration(
    f, initial_guess: float, tolerance: float = 1e-5, max_iterations: int = 1000
) -> float:
    """
    Calculate the fixed point of a function using the fixed-point iteration method.

    :param f: The function for which to find a fixed point. It takes a single argument and returns a float.
    :param initial_guess: The initial guess for the fixed point.
    :param tolerance: The tolerance for the difference between successive approximations. Defaults to 1e-5.
    :param max_iterations: The maximum number of iterations to perform. Defaults to 1000.
    :return: The approximated fixed point of the function.
    """
    x0 = initial_guess
    for _ in range(max_iterations):
        x1 = f(x0)
        if abs(x1 - x0) < tolerance:
            return x1
        x0 = x1
    return x0


# logic


def calculate_modulus(a: int, b: int) -> int:
    """
    Calculate the modulus of two integers.

    :param a: The dividend in the modulus operation.
    :param b: The divisor in the modulus operation.
    :return: The remainder after dividing `a` by `b`.
    """
    return a % b


def calculate_power(base: float, exponent: float) -> float:
    """
    Calculate the power of a base raised to a given exponent.

    :param base: The base value.
    :param exponent: The exponent value.
    :return: The result of `base` raised to the power of `exponent`.
    """
    return base**exponent


def find_greatest_common_divisor(a: int, b: int) -> int:
    """
    Find the greatest common divisor (GCD) of two integers.

    :param a: First integer.
    :param b: Second integer.
    :return: The greatest common divisor of `a` and `b`.
    """
    while b:
        a, b = b, a % b
    return a


def calculate_modular_sum(a: int, b: int, m: int) -> int:
    """
    Calculate the sum of two numbers under modular arithmetic.

    :param a: The first number.
    :param b: The second number.
    :param m: The modulus.
    :return: The sum of a and b under modulus m.
    """
    return (a + b) % m


def calculate_xor(a: int, b: int) -> int:
    """
    Calculate the bitwise XOR of two integers.

    :param a: The first integer.
    :param b: The second integer.
    :return: The result of a XOR b.
    """
    return a ^ b


def calculate_factorial_division(n: int, k: int) -> int:
    """
    Calculate the division of factorial n by factorial k, assuming n >= k.

    :param n: The numerator factorial parameter.
    :param k: The denominator factorial parameter.
    :return: The result of n! / k!.
    """
    result = 1
    for i in range(k + 1, n + 1):
        result *= i
    return result


def calculate_log_base_n(x: float, n: float) -> float:
    """
    Calculate the logarithm of x to the base n.

    :param x: The number to find the logarithm of.
    :param n: The base of the logarithm.
    :return: The logarithm of x to the base n.
    """
    import math

    return math.log(x) / math.log(n)


def calculate_inverse_modulo(a: int, m: int) -> int:
    """
    Calculate the modular multiplicative inverse of a under modulo m.

    :param a: The number to find the inverse of.
    :param m: The modulo.
    :return: The modular multiplicative inverse of a modulo m.
    """
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1


def calculate_power_modulo(base: int, exponent: int, modulo: int) -> int:
    """
    Calculate the power of a base raised to an exponent under a modulo.

    :param base: The base number.
    :param exponent: The exponent.
    :param modulo: The modulo.
    :return: The result of (base^exponent) % modulo.
    """
    result = 1
    base = base % modulo
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulo
        exponent = exponent // 2
        base = (base * base) % modulo
    return result


def calculate_nth_fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.

    :param n: The position of the Fibonacci number to find.
    :return: The nth Fibonacci number.
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def calculate_modular_multiplication(a: int, b: int, mod: int) -> int:
    """
    Calculate the modular multiplication of two numbers.

    :param a: The first number to multiply.
    :param b: The second number to multiply.
    :param mod: The modulus to apply.
    :return: The result of (a * b) % mod.
    """
    return (a * b) % mod


def calculate_inverse_cosine(x: float) -> float:
    """
    Calculate the arc cosine (inverse cosine) of a number.

    :param x: The number to calculate the arc cosine for, where -1 <= x <= 1.
    :return: The arc cosine of x in radians.
    """
    import math

    return math.acos(x)


def calculate_logarithm_base_10(x: float) -> float:
    """
    Calculate the base 10 logarithm of a number.

    :param x: The number to calculate the logarithm for, must be > 0.
    :return: The base 10 logarithm of x.
    """
    import math

    return math.log10(x)


def calculate_sine_hyperbolic(x: float) -> float:
    """
    Calculate the hyperbolic sine of a number.

    :param x: The number to calculate the hyperbolic sine for.
    :return: The hyperbolic sine of x.
    """
    import math

    return math.sinh(x)


def calculate_cubic_equation(a: float, b: float, c: float, d: float) -> list:
    """
    Solve a cubic equation of the form ax^3 + bx^2 + cx + d = 0.

    :param a: Coefficient of x^3.
    :param b: Coefficient of x^2.
    :param c: Coefficient of x.
    :param d: Constant term.
    :return: A list containing the roots of the cubic equation.
    """
    import numpy as np

    # Coefficients in descending powers
    coeffs = [a, b, c, d]
    # Solve cubic equation
    roots = np.roots(coeffs)
    return roots.tolist()


def calculate_logistic_growth(
    initial_population: float, growth_rate: float, carrying_capacity: float, time: float
) -> float:
    """
    Calculate the population at a given time using the logistic growth model.

    This function models population growth that starts exponentially but levels off
    as the population approaches a carrying capacity.

    :param initial_population: The initial population size
    :param growth_rate: The rate at which the population grows
    :param carrying_capacity: The maximum population size that the environment can sustain
    :param time: The time at which to calculate the population
    :return: The population at the given time
    """
    import math

    return (carrying_capacity * initial_population * math.exp(growth_rate * time)) / (
        carrying_capacity + initial_population * (math.exp(growth_rate * time) - 1)
    )


def calculate_cubic_equation_roots(a: float, b: float, c: float, d: float) -> tuple:
    """
    Calculate the roots of a cubic equation of the form ax^3 + bx^2 + cx + d = 0.

    This function uses the general solution to the cubic equation to find its roots.

    :param a: The coefficient of the cubic term
    :param b: The coefficient of the quadratic term
    :param c: The coefficient of the linear term
    :param d: The constant term
    :return: A tuple containing the roots of the cubic equation
    """
    import math

    f = ((3 * c / a) - (b**2 / a**2)) / 3
    g = ((2 * b**3 / a**3) - (9 * b * c / a**2) + (27 * d / a)) / 27
    h = (g**2 / 4) + (f**3 / 27)

    if h > 0:
        R = -(g / 2) + math.sqrt(h)
        S = R ** (1 / 3)
        T = -(g / 2) - math.sqrt(h)
        U = T ** (1 / 3)
        root = (S + U) - (b / (3 * a))
        return (root,)
    else:
        raise NotImplementedError


def calculate_modular_subtraction(a: int, b: int, m: int) -> int:
    """
    Calculate the subtraction of two numbers modulo m.

    :param a: The minuend in the subtraction.
    :param b: The subtrahend in the subtraction.
    :param m: The modulus.
    :return: The result of (a - b) mod m.
    """
    return (a - b) % m


def calculate_inverse_tangent(x: float) -> float:
    """
    Calculate the inverse tangent (arctan) of a number.

    :param x: The number to calculate the arctan for.
    :return: The arctan of x.
    """
    import math

    return math.atan(x)


def calculate_logarithm_base_2(x: float) -> float:
    """
    Calculate the base 2 logarithm of a number.

    :param x: The number to calculate the logarithm for.
    :return: The base 2 logarithm of x.
    """
    import math

    return math.log2(x)


def calculate_nth_power(x: float, n: int) -> float:
    """
    Calculate the nth power of a number.

    :param x: The base number.
    :param n: The exponent to raise the base to.
    :return: The result of x raised to the power of n.
    """
    return x**n


def calculate_cubic_polynomial_value(
    a: float, b: float, c: float, d: float, x: float
) -> float:
    """
    Calculate the value of a cubic polynomial a*x^3 + b*x^2 + c*x + d at a given x.

    :param a: Coefficient of x^3.
    :param b: Coefficient of x^2.
    :param c: Coefficient of x.
    :param d: Constant term.
    :param x: The value at which to evaluate the polynomial.
    :return: The value of the cubic polynomial at x.
    """
    return a * x**3 + b * x**2 + c * x + d


def calculate_geometric_progression_nth_term(a: float, r: float, n: int) -> float:
    """
    Calculate the nth term of a geometric progression.

    :param a: The first term of the geometric progression.
    :param r: The common ratio of the geometric progression.
    :param n: The term number to find.
    :return: The nth term of the geometric progression.
    """
    return a * r ** (n - 1)


def calculate_arithmetic_progression_nth_term(a: float, d: float, n: int) -> float:
    """
    Calculate the nth term of an arithmetic progression.

    :param a: The first term of the arithmetic progression.
    :param d: The common difference of the arithmetic progression.
    :param n: The term number to find.
    :return: The nth term of the arithmetic progression.
    """
    return a + (n - 1) * d


def calculate_modular_gcd(a: int, b: int, m: int) -> int:
    """
    Calculate the greatest common divisor (GCD) of two numbers a and b, then take the result modulo m.

    :param a: First number
    :param b: Second number
    :param m: Modulus value
    :return: The GCD of a and b, taken modulo m
    """
    while b:
        a, b = b, a % b
    return a % m


def calculate_least_nonnegative_residue(n: int, m: int) -> int:
    """
    Calculate the least nonnegative residue of n modulo m.

    :param n: The integer whose residue is to be found
    :param m: The modulus
    :return: The least nonnegative residue of n modulo m
    """
    return n % m


def calculate_inverse_mod_n(a: int, n: int) -> int:
    """
    Calculate the modular multiplicative inverse of a modulo n, if it exists.

    :param a: The number to find the inverse for
    :param n: The modulus
    :return: The modular multiplicative inverse of a modulo n, or -1 if it does not exist
    """
    for i in range(1, n):
        if (a * i) % n == 1:
            return i
    return -1


def calculate_modular_addition(a: int, b: int, mod: int) -> int:
    """
    Calculate the modular addition of two numbers.

    :param a: The first number to be added.
    :param b: The second number to be added.
    :param mod: The modulus to be applied.
    :return: The result of (a + b) % mod.
    """
    return (a + b) % mod


def calculate_inverse_square(x: float) -> float:
    """
    Calculate the inverse square of a number.

    :param x: The number to calculate the inverse square of.
    :return: The inverse square of x, which is 1 / x^2.
    """
    return 1 / (x**2)


def calculate_geometric_series_sum(a: float, r: float, n: int) -> float:
    """
    Calculate the sum of the first n terms of a geometric series.

    :param a: The first term of the geometric series.
    :param r: The common ratio of the geometric series.
    :param n: The number of terms to sum.
    :return: The sum of the first n terms of the geometric series.
    """
    if r == 1:
        return a * n
    else:
        return a * (1 - r**n) / (1 - r)


def calculate_logarithmic_sum(n: int) -> float:
    """
    Calculate the sum of logarithms of all natural numbers up to n.

    :param n: The upper limit of the natural numbers to calculate the logarithm sum for.
    :return: The sum of logarithms of all natural numbers up to n.
    """
    import math

    return sum(math.log(i) for i in range(1, n + 1))


def calculate_harmonic_number(n: int) -> float:
    """
    Calculate the nth harmonic number.

    :param n: The order of the harmonic number to calculate.
    :return: The nth harmonic number.
    """
    return sum(1 / i for i in range(1, n + 1))


def calculate_least_squares_regression_line(
    points: list[tuple[float, float]]
) -> tuple[float, float]:
    """
    Calculate the slope and intercept of the least squares regression line for a set of points.

    :param points: A list of tuples, where each tuple represents a point (x, y).
    :return: A tuple containing the slope and intercept of the regression line.
    """
    n = len(points)
    sum_x = sum(point[0] for point in points)
    sum_y = sum(point[1] for point in points)
    sum_xy = sum(point[0] * point[1] for point in points)
    sum_x_squared = sum(point[0] ** 2 for point in points)
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
    intercept = (sum_y - slope * sum_x) / n
    return slope, intercept


def calculate_coprimes(n: int) -> list[int]:
    """
    Calculate all coprime numbers of a given number n.

    :param n: The number to find coprimes for.
    :return: A list of numbers that are coprime to n.
    """

    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    return [x for x in range(1, n) if gcd(x, n) == 1]


def calculate_euclidean_distance_2d(
    x1: float, y1: float, x2: float, y2: float
) -> float:
    """
    Calculate the Euclidean distance between two points in 2D space.

    :param x1: The x-coordinate of the first point.
    :param y1: The y-coordinate of the first point.
    :param x2: The x-coordinate of the second point.
    :param y2: The y-coordinate of the second point.
    :return: The Euclidean distance between the two points.
    """
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def calculate_nth_triangular_number(n: int) -> int:
    """
    Calculate the nth triangular number.

    :param n: The term of the triangular number to calculate.
    :return: The nth triangular number.
    """
    return n * (n + 1) // 2


def calculate_coprime_count(n: int) -> int:
    """
    Calculate the number of positive integers less than or equal to n that are coprime to n.

    :param n: The integer to find coprimes for.
    :return: The count of positive integers less than or equal to n that are coprime to n.
    """
    count = 0
    for i in range(1, n + 1):
        if gcd(n, i) == 1:
            count += 1
    return count


def calculate_harmonic_progression_nth_term(a: float, d: float, n: int) -> float:
    """
    Calculate the nth term of a harmonic progression.

    The formula used is: 1 / (1/a + (n-1)*d)

    :param a: The first term of the harmonic progression.
    :param d: The common difference of the harmonic progression.
    :param n: The term number to find.
    :return: The nth term of the harmonic progression.
    """
    return 1 / (1 / a + (n - 1) * d)


def calculate_logarithmic_series(n: int, x: float) -> float:
    """
    Calculate the sum of the first n terms of the logarithmic series (natural log).

    The series is: ln(1+x) = x - x^2/2 + x^3/3 - x^4/4 + ... + (-1)^(n+1) * x^n/n

    :param n: The number of terms in the series.
    :param x: The value to compute the logarithmic series for.
    :return: The sum of the first n terms of the logarithmic series.
    """
    sum_series = 0
    for i in range(1, n + 1):
        sum_series += ((-1) ** (i + 1) * x**i) / i
    return sum_series


def calculate_cubic_sum(n: int) -> int:
    """
    Calculate the sum of the first n cubic numbers.

    The formula used is: (n(n+1)/2)^2

    :param n: The number of cubic numbers to sum.
    :return: The sum of the first n cubic numbers.
    """
    return (n * (n + 1) // 2) ** 2


def calculate_modular_multiplicative_inverse(a: int, m: int) -> int:
    """
    Calculate the modular multiplicative inverse of a under modulo m.

    The modular multiplicative inverse of an integer a modulo m is an integer x such that
    the product ax is congruent to 1 modulo m. This function finds such an x, if it exists.

    :param a: The integer whose modular multiplicative inverse is to be found.
    :param m: The modulo.
    :return: The modular multiplicative inverse of a under modulo m if it exists, otherwise -1.
    """
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1


def calculate_least_squares_slope(
    x_values: list[float], y_values: list[float]
) -> float:
    """
    Calculate the slope of the least squares regression line for a given set of data points.

    The least squares regression line is the line that minimizes the sum of the squares of the
    vertical distances of the points from the line. This function calculates the slope of that line.

    :param x_values: A list of x-coordinates of the data points.
    :param y_values: A list of y-coordinates of the data points.
    :return: The slope of the least squares regression line.
    """
    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x_squared = sum(x**2 for x in x_values)
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
    return slope


def calculate_nth_power_sum(n: int, power: int) -> int:
    """
    Calculate the sum of the first n natural numbers raised to a given power.

    This function computes the sum of the series 1^power + 2^power + ... + n^power.

    :param n: The number of terms in the series.
    :param power: The power to which each term is raised.
    :return: The sum of the series.
    """
    return sum(i**power for i in range(1, n + 1))


def calculate_vector_magnitude(vector: list[float]) -> float:
    """
    Calculate the magnitude (or length) of a vector.

    The magnitude of a vector is the square root of the sum of the squares of its components.
    This function calculates the magnitude of a given vector.

    :param vector: A list of components of the vector.
    :return: The magnitude of the vector.
    """
    from math import sqrt

    return sqrt(sum(component**2 for component in vector))


def calculate_hypotenuse_length(a: float, b: float) -> float:
    """
    Calculate the length of the hypotenuse of a right-angled triangle given the lengths of the other two sides.

    This function uses the Pythagorean theorem to calculate the length of the hypotenuse.

    :param a: The length of one of the sides of the right-angled triangle.
    :param b: The length of the other side of the right-angled triangle.
    :return: The length of the hypotenuse.
    """
    return (a**2 + b**2) ** 0.5


def calculate_least_squares_regression_intercept(
    x_values: list[float], y_values: list[float]
) -> float:
    """
    Calculate the y-intercept (b0) of the least squares regression line from given x and y values.

    :param x_values: A list of x-coordinates.
    :param y_values: A list of y-coordinates.
    :return: The y-intercept of the least squares regression line.
    """
    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x_squared = sum(x**2 for x in x_values)
    b1 = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
    b0 = (sum_y - b1 * sum_x) / n
    return b0


def calculate_vector_length(vector: list[float]) -> float:
    """
    Calculate the length (magnitude) of a vector.

    :param vector: A list of numbers representing the vector components.
    :return: The length of the vector.
    """
    return sum(component**2 for component in vector) ** 0.5


def calculate_least_squares_regression_slope(x: list[float], y: list[float]) -> float:
    """
    Calculate the slope of the least squares regression line for a given set of data points.

    The slope of the least squares regression line is given by the formula:
    (n*Σ(xy) - Σx*Σy) / (n*Σ(x^2) - (Σx)^2), where n is the number of data points.

    :param x: A list of x-coordinates of the data points.
    :param y: A list of y-coordinates of the data points.
    :return: The slope of the least squares regression line.
    """
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x_squared = sum(x[i] ** 2 for i in range(n))
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
    return slope


def calculate_vector_dot_product(vector_a: list[float], vector_b: list[float]) -> float:
    """
    Calculate the dot product of two vectors.

    The dot product of two vectors is the sum of the products of their corresponding entries.

    :param vector_a: A list representing the first vector.
    :param vector_b: A list representing the second vector.
    :return: The dot product of the two vectors.
    """
    return sum(a * b for a, b in zip(vector_a, vector_b))


def calculate_mean_absolute_deviation(data: list[float]) -> float:
    """
    Calculate the mean absolute deviation of a dataset.

    The mean absolute deviation is the average of the absolute deviations from the mean of the dataset.

    :param data: A list of numbers representing the dataset.
    :return: The mean absolute deviation of the dataset.
    """
    mean = sum(data) / len(data)
    return sum(abs(x - mean) for x in data) / len(data)


def calculate_euclidean_norm(vector: list[float]) -> float:
    """
    Calculate the Euclidean norm (or Euclidean length) of a vector.

    The Euclidean norm of a vector is the square root of the sum of the squares of its components.

    :param vector: A list representing the vector.
    :return: The Euclidean norm of the vector.
    """
    return sum(component**2 for component in vector) ** 0.5


def calculate_circular_sector_perimeter(radius: float, angle: float) -> float:
    """
    Calculate the perimeter of a circular sector given its radius and central angle.

    The perimeter of a circular sector is the sum of the lengths of the two radii and the arc length,
    which can be calculated as (angle/360) * 2 * π * radius for the arc length, where angle is in degrees.

    :param radius: The radius of the circular sector.
    :param angle: The central angle of the circular sector in degrees.
    :return: The perimeter of the circular sector.
    """
    from math import pi

    arc_length = (angle / 360) * 2 * pi * radius
    return 2 * radius + arc_length


def calculate_greatest_common_divisor(a: int, b: int) -> int:
    """
    Calculate the Greatest Common Divisor (GCD) of two integers.

    The GCD of two integers a and b is the largest positive integer that divides both
    a and b without leaving a remainder.

    :param a: First integer.
    :param b: Second integer.
    :return: The GCD of a and b.
    """
    while b:
        a, b = b, a % b
    return a


# set_theory


def union_of_sets(set_a: set[str], set_b: set[str]) -> set:
    """
    Calculate the union of two sets.

    :param set_a: The first set
    :param set_b: The second set
    :return: A set containing all elements that are in set_a, set_b, or both
    """
    return set_a.union(set_b)


def intersection_of_sets(set_a: set[str], set_b: set[str]) -> set:
    """
    Calculate the intersection of two sets.

    :param set_a: The first set
    :param set_b: The second set
    :return: A set containing all elements that are in both set_a and set_b
    """
    return set_a.intersection(set_b)


def difference_of_sets(set_a: set[str], set_b: set[str]) -> set:
    """
    Calculate the difference between two sets.

    :param set_a: The first set from which elements will be subtracted
    :param set_b: The second set whose elements will be subtracted from the first set
    :return: A set containing all elements that are in set_a but not in set_b
    """
    return set_a.difference(set_b)


def symmetric_difference_of_sets(set_a: set[str], set_b: set[str]) -> set:
    """
    Calculate the symmetric difference of two sets.

    :param set_a: The first set
    :param set_b: The second set
    :return: A set containing all elements that are in either set_a or set_b but not in both
    """
    return set_a.symmetric_difference(set_b)


def is_disjoint(set_a: set[str], set_b: set[str]) -> bool:
    """
    Determine if two sets have no elements in common.

    :param set_a: First set
    :param set_b: Second set
    :return: True if A and B have no common elements, False otherwise
    """
    return set_a.isdisjoint(set_b)


def set_complement(universal_set: set[str], subset: set[str]) -> set:
    """
    Calculate the complement of a subset within a universal set.

    :param universal_set: The universal set from which the subset is derived.
    :param subset: The subset for which the complement is to be found.
    :return: The complement of the subset within the universal set.
    """
    return universal_set - subset


def cartesian_product(set_a: set[str], set_b: set[str]) -> set:
    """
    Calculate the Cartesian product of two sets.

    :param set_a: The first set.
    :param set_b: The second set.
    :return: The Cartesian product of set_a and set_b.
    """
    return {(a, b) for a in set_a for b in set_b}


def power_set(input_set: set[str]) -> set:
    """
    Calculate the power set of a given set.

    :param input_set: The set for which the power set is to be calculated.
    :return: The power set of the input set.
    """
    from itertools import chain, combinations

    return {
        frozenset(comb)
        for comb in chain.from_iterable(
            combinations(input_set, r) for r in range(len(input_set) + 1)
        )
    }


def is_superset(super_set: set[str], sub_set: set[str]) -> bool:
    """
    Determine if one set is a superset of another.

    :param super_set: The set that might be a superset.
    :param sub_set: The set that might be a subset.
    :return: True if super_set is a superset of sub_set, False otherwise.
    """
    return super_set.issuperset(sub_set)


def is_proper_subset(sub_set: set[str], super_set: set[str]) -> bool:
    """
    Determine if one set is a proper subset of another.

    :param sub_set: The set that might be a proper subset.
    :param super_set: The set that might be a superset.
    :return: True if sub_set is a proper subset of super_set, False otherwise.
    """
    return sub_set.issubset(super_set) and sub_set != super_set


def set_cardinality(s: set[str]) -> int:
    """
    Calculate the cardinality (number of elements) of a set.

    :param s: The set whose cardinality is to be found
    :return: The cardinality of the set
    """
    return len(s)


def is_element_of_set(element: int, s: set[int]) -> bool:
    """
    Check if an element is a member of a given set.

    :param element: The element to check
    :param s: The set to check in
    :return: True if the element is in the set, False otherwise
    """
    return element in s


def set_power_set(s: set[str]) -> set:
    """
    Calculate the power set of a given set. The power set contains all subsets of a set.

    :param s: The set to calculate the power set of
    :return: The power set of the given set
    """
    from itertools import chain, combinations

    return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def disjoint_sets(s1: set[str], s2: set[str]) -> bool:
    """
    Determine if two sets are disjoint. Two sets are disjoint if they have no elements in common.

    :param s1: The first set
    :param s2: The second set
    :return: True if the sets are disjoint, False otherwise
    """
    return s1.isdisjoint(s2)


def cartesian_product_set(s1: set[str], s2: set[str]) -> set:
    """
    Calculate the Cartesian product of two sets. The Cartesian product of two sets is a set of all ordered pairs
    where the first element of each pair is from the first set and the second element is from the second set.

    :param s1: The first set
    :param s2: The second set
    :return: The Cartesian product of the two sets
    """
    from itertools import product

    return set(product(s1, s2))


def set_is_empty(s: set[str]) -> bool:
    """
    Determine if a given set is empty.

    :param s: The set to check
    :return: True if the set is empty, False otherwise
    """
    return len(s) == 0


def set_max_element(s: set[int]) -> int:
    """
    Find the maximum element in a non-empty set of integers.

    :param s: The set of integers
    :return: The maximum element in the set
    """
    return max(s)


def set_min_element(s: set[int]) -> int:
    """
    Find the minimum element in a non-empty set of integers.

    :param s: The set of integers
    :return: The minimum element in the set
    """
    return min(s)


def set_element_belongs(s: set[int], element: int) -> bool:
    """
    Check if an element belongs to a set.

    :param s: The set to check
    :param element: The element to look for in the set
    :return: True if the element is in the set, False otherwise
    """
    return element in s


def set_clear(s: set[str]) -> set:
    """
    Clear all elements from a set, making it an empty set.

    :param s: The set to clear
    :return: An empty set
    """
    s.clear()
    return s


def set_relative_complement(set_a: set[str], set_b: set[str]) -> set:
    """
    Calculate the relative complement of set B in set A.

    The relative complement of set_b in set_a (also called the set difference of set_a and set_b)
    is the set of elements in set_a, but not in set_b.

    :param set_a: The first set
    :param set_b: The second set
    :return: A set containing elements that are in set_a but not in set_b
    """
    return set_a.difference(set_b)


def is_proper_superset(set_a: set[str], set_b: set[str]) -> bool:
    """
    Determine if set_a is a proper superset of set_b.

    A proper superset of a set is a superset that is not equal to the initial set.

    :param set_a: The first set
    :param set_b: The second set
    :return: True if set_a is a proper superset of set_b, False otherwise
    """
    return set_a > set_b


def set_cartesian_product(set_a: set[str], set_b: set[str]) -> set:
    """
    Calculate the Cartesian product of two sets A and B.

    The Cartesian product of set_a and set_b is the set of all possible ordered pairs
    where the first element is from set_a and the second element is from set_b.

    :param set_a: The first set
    :param set_b: The second set
    :return: A set of tuples representing the Cartesian product of set_a and set_b
    """
    return {(a, b) for a in set_a for b in set_b}


def set_is_disjoint(set_a: set[str], set_b: set[str]) -> bool:
    """
    Determine if two sets set_a and set_b are disjoint.

    Two sets are disjoint if they have no elements in common.

    :param set_a: The first set
    :param set_b: The second set
    :return: True if set_a and set_b are disjoint, False otherwise
    """
    return set_a.isdisjoint(set_b)


def set_union_multiple(sets: list[set[str]]) -> set:
    """
    Find the union of multiple sets.

    :param sets: An arbitrary number of sets to find the union of.
    :return: A set containing all unique elements from all provided sets.
    """
    return set().union(sets)


def set_intersection_multiple(sets: list[set[str]]) -> set:
    """
    Find the intersection of multiple sets.

    :param sets: An arbitrary number of sets to find the intersection of.
    :return: A set containing all elements common to all provided sets.
    """
    if not sets:
        return set()
    return set().intersection(sets)


def set_union(a: set[str], b: set[str]) -> set:
    """
    Returns the union of two sets.

    :param a: First set
    :param b: Second set
    :return: A set containing all elements from both a and b
    """
    return a.union(b)


def set_intersection(a: set[str], b: set[str]) -> set:
    """
    Returns the intersection of two sets.

    :param a: First set
    :param b: Second set
    :return: A set containing all elements that are in both a and b
    """
    return a.intersection(b)


def set_difference(a: set[str], b: set[str]) -> set:
    """
    Returns the difference of two sets.

    :param a: First set from which elements are taken
    :param b: Second set whose elements are removed from the first set
    :return: A set containing all elements of a that are not in b
    """
    return a.difference(b)


def set_symmetric_difference(a: set[str], b: set[str]) -> set:
    """
    Returns the symmetric difference of two sets.

    :param a: First set
    :param b: Second set
    :return: A set containing all elements that are in either a or b but not in both
    """
    return a.symmetric_difference(b)


def is_subset(a: set[str], b: set[str]) -> bool:
    """
    Determines if set a is a subset of set b.

    :param a: The set to test if it is a subset
    :param b: The set to test against
    :return: True if a is a subset of b, False otherwise
    """
    return a.issubset(b)


def set_is_equal(set_a: set[str], set_b: set[str]) -> bool:
    """
    Determine if two sets are equal.

    :param set_a: First set to compare
    :param set_b: Second set to compare
    :return: True if sets set_a and set_b contain exactly the same elements, False otherwise
    """
    return set_a == set_b


def set_subset_relation(set_a: set[str], set_b: set[str]) -> str:
    """
    Determine the subset relation between two sets.

    :param set_a: First set
    :param set_b: Second set
    :return: A string indicating the subset relation.
    """
    if set_a == set_b:
        return "set_a and set_b are equal"
    elif set_a.issubset(set_b):
        return "set_a is a subset of set_b"
    elif set_b.issubset(set_a):
        return "set_b is a subset of set_a"
    else:
        return "No subset relation"


def set_complement_universe(set_a: set[str], set_u: set[str]) -> set:
    """
    Calculate the complement of a set_a with respect to the universe set set_u.

    :param set_a: The set for which to find the complement
    :param set_u: The universe set relative to which the complement is calculated
    :return: The complement of set_a with respect to set_u
    """
    return set_u - set_a


def set_is_proper_superset(set_a: set[str], set_b: set[str]) -> bool:
    """
    Determine if set_a is a proper superset of set_b.

    :param set_a: The first set to be compared.
    :param set_b: The second set, which is compared against the first set.
    :return: True if set_a is a proper superset of set_b, False otherwise.
    """
    return set_a > set_b


def symmetric_difference(set_a: set[str], set_b: set[str]) -> set:
    """
    Calculate the symmetric difference between two sets set_a and set_b.

    :param set_a: The first set.
    :param set_b: The second set.
    :return: A new set containing elements that are in either set_a or set_b but not in both.
    """
    return set_a.symmetric_difference(set_b)


# probability theory


def calculate_probability_of_union(A: float, B: float, intersection: float) -> float:
    """
    Calculate the probability of the union of two events.

    :param A: Probability of event A
    :param B: Probability of event B
    :param intersection: Probability of the intersection of A and B
    :return: Probability of the union of A and B
    """
    return A + B - intersection


def calculate_bayes_theorem(P_A: float, P_B_given_A: float, P_B: float) -> float:
    """
    Apply Bayes' theorem to calculate the probability of A given B.

    :param P_A: Probability of event A
    :param P_B_given_A: Probability of event B given A
    :param P_B: Probability of event B
    :return: Probability of A given B
    """
    return (P_B_given_A * P_A) / P_B


def calculate_combination(n: int, r: int) -> int:
    """
    Calculate the number of combinations of n items taken r at a time.

    :param n: Total number of items
    :param r: Number of items to take
    :return: Number of combinations
    """
    from math import factorial

    return factorial(n) // (factorial(r) * factorial(n - r))


def calculate_event_probability(event_outcomes: int, sample_space: int) -> float:
    """
    Calculate the probability of an event occurring.

    :param event_outcomes: Number of favorable outcomes for the event.
    :param sample_space: Total number of outcomes in the sample space.
    :return: The probability of the event occurring.
    """
    return event_outcomes / sample_space


def calculate_independent_events_probability(p_a: float, p_b: float) -> float:
    """
    Calculate the probability of two independent events both occurring.

    :param p_a: Probability of event A occurring.
    :param p_b: Probability of event B occurring.
    :return: The probability of both event A and event B occurring.
    """
    return p_a * p_b


def calculate_conditional_probability(p_a_given_b: float, p_b: float) -> float:
    """
    Calculate the conditional probability of event A occurring given that event B has occurred.

    :param p_a_given_b: Probability of event A occurring given event B.
    :param p_b: Probability of event B occurring.
    :return: The conditional probability of event A given event B.
    """
    return p_a_given_b * p_b


def calculate_permutation_count(n: int, r: int) -> int:
    """
    Calculate the number of ways to choose a sample of r items from a set of n items
    without replacement and where the order of selection matters.

    :param n: Total number of items.
    :param r: Number of items to select.
    :return: The number of permutations.
    """
    from math import factorial

    return factorial(n) // factorial(n - r)


def calculate_combination_count(n: int, r: int) -> int:
    """
    Calculate the number of ways to choose a sample of r items from a set of n items
    without replacement and where the order of selection does not matter.

    :param n: Total number of items.
    :param r: Number of items to select.
    :return: The number of combinations.
    """
    from math import factorial

    return factorial(n) // (factorial(r) * factorial(n - r))


def calculate_probability(success_outcomes: int, total_outcomes: int) -> float:
    """
    Calculate the probability of an event given the number of successful outcomes and the total number of outcomes.

    :param success_outcomes: Number of successful outcomes.
    :param total_outcomes: Total number of outcomes.
    :return: The probability of the event.
    """
    return success_outcomes / total_outcomes


def calculate_expected_value(
    probabilities: list[float], outcomes: list[float]
) -> float:
    """
    Calculate the expected value of a random variable, given a list of probabilities and their corresponding outcomes.

    :param probabilities: A list of probabilities for each outcome.
    :param outcomes: A list of outcomes.
    :return: The expected value.
    """
    return sum(p * x for p, x in zip(probabilities, outcomes))


def calculate_variance_of_discrete_random_variable(
    probabilities: list[float], outcomes: list[float], expected_value: float
) -> float:
    """
    Calculate the variance of a discrete random variable given a list of probabilities,
    their corresponding outcomes, and the expected value of the random variable.

    :param probabilities: A list of probabilities for each outcome.
    :param outcomes: A list of outcomes.
    :param expected_value: The expected value of the random variable.
    :return: The variance of the random variable.
    """
    return sum(p * ((x - expected_value) ** 2) for p, x in zip(probabilities, outcomes))


def calculate_joint_probability(p_a: float, p_b_given_a: float) -> float:
    """
    Calculate the joint probability of two events, A and B, occurring together,
    given the probability of A and the conditional probability of B given A.

    :param p_a: Probability of event A
    :param p_b_given_a: Conditional probability of event B given A
    :return: Joint probability of events A and B
    """
    return p_a * p_b_given_a


def calculate_marginal_probability(
    p_a: float, p_b_given_a: float, p_b_given_not_a: float
) -> float:
    """
    Calculate the marginal probability of event B from the total probability theorem,
    given the probability of event A, the conditional probability of B given A,
    and the conditional probability of B given not A.

    :param p_a: Probability of event A
    :param p_b_given_a: Conditional probability of event B given A
    :param p_b_given_not_a: Conditional probability of event B given not A
    :return: Marginal probability of event B
    """
    return p_a * p_b_given_a + (1 - p_a) * p_b_given_not_a


def calculate_posterior_probability(
    p_a: float, p_b_given_a: float, p_b: float
) -> float:
    """
    Calculate the posterior probability of event A given event B has occurred,
    using Bayes' theorem.

    :param p_a: Probability of event A
    :param p_b_given_a: Conditional probability of event B given A
    :param p_b: Marginal probability of event B
    :return: Posterior probability of event A given B
    """
    return (p_b_given_a * p_a) / p_b


def calculate_variance_of_binomial_distribution(n: int, p: float) -> float:
    """
    Calculate the variance of a binomial distribution.

    :param n: Number of trials
    :param p: Probability of success on a single trial
    :return: Variance of the binomial distribution
    """
    return n * p * (1 - p)


def calculate_standard_deviation_of_binomial_distribution(n: int, p: float) -> float:
    """
    Calculate the standard deviation of a binomial distribution.

    :param n: Number of trials
    :param p: Probability of success on a single trial
    :return: Standard deviation of the binomial distribution
    """
    from math import sqrt

    return sqrt(n * p * (1 - p))


def calculate_hypergeometric_probability(N: int, K: int, n: int, k: int) -> float:
    """
    Calculate the hypergeometric probability, which is the probability of k successes
    in n draws, without replacement, from a finite population of size N that contains
    exactly K successes.

    :param N: Population size.
    :param K: Number of successes in the population.
    :param n: Number of draws.
    :param k: Number of observed successes.
    :return: Hypergeometric probability.
    """
    from math import comb

    return comb(K, k) * comb(N - K, n - k) / comb(N, n)


def calculate_negative_binomial_probability(r: int, k: int, p: float) -> float:
    """
    Calculate the negative binomial probability, which is the probability of k
    failures and r successes in k + r Bernoulli trials, with success on the (k+r)th trial.

    :param r: Number of successes.
    :param k: Number of failures.
    :param p: Probability of success on a single trial.
    :return: Negative binomial probability.
    """
    from math import comb

    return comb(k + r - 1, r - 1) * (p**r) * ((1 - p) ** k)


def calculate_probability_of_no_success(p_success: float, trials: int) -> float:
    """
    Calculate the probability of no success in a given number of trials,
    given the probability of success in a single trial.

    :param p_success: The probability of success in a single trial.
    :param trials: The number of trials.
    :return: The probability of no success.
    """
    return (1 - p_success) ** trials


def calculate_mean_of_discrete_random_variable(
    values: list[int], probabilities: list[float]
) -> float:
    """
    Calculate the mean (expected value) of a discrete random variable.

    :param values: A list of the discrete random variable's values.
    :param probabilities: A list of probabilities associated with each value.
    :return: The mean (expected value) of the discrete random variable.
    """
    return sum(value * probability for value, probability in zip(values, probabilities))


def calculate_uniform_distribution_probability(a: float, b: float, x: float) -> float:
    """
    Calculate the probability density function of a uniform distribution.

    :param a: Lower bound of the distribution.
    :param b: Upper bound of the distribution.
    :param x: Point at which to evaluate the density.
    :return: The probability density at point x.
    """
    if a <= x <= b:
        return 1 / (b - a)
    else:
        return 0


def calculate_poisson_distribution_probability(lambda_: float, k: int) -> float:
    """
    Calculate the probability of observing k events in a fixed interval of time
    or space, given the average number of events per interval (lambda).

    :param lambda_: The average number of events per interval.
    :param k: The number of events observed.
    :return: The probability of observing k events.
    """
    from math import exp, factorial

    return (lambda_**k) * exp(-lambda_) / factorial(k)


def calculate_normal_distribution_probability(
    mu: float, sigma: float, x: float
) -> float:
    """
    Calculate the probability density function of a normal distribution.

    :param mu: Mean of the distribution.
    :param sigma: Standard deviation of the distribution.
    :param x: Point at which to evaluate the density.
    :return: The probability density at point x.
    """
    from math import exp, pi, sqrt

    return exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * sqrt(2 * pi))


def calculate_exponential_distribution_probability(lambda_: float, x: float) -> float:
    """
    Calculate the probability density function of an exponential distribution.

    :param lambda_: The rate parameter, which is the inverse of the mean.
    :param x: Point at which to evaluate the density.
    :return: The probability density at point x.
    """
    from math import exp

    if x < 0:
        return 0
    else:
        return lambda_ * exp(-lambda_ * x)


def calculate_uniform_distribution_mean(a: float, b: float) -> float:
    """
    Calculate the mean (expected value) of a uniform distribution.

    :param a: Lower bound of the distribution.
    :param b: Upper bound of the distribution.
    :return: The mean of the uniform distribution.
    """
    return (a + b) / 2


def calculate_uniform_distribution_variance(a: float, b: float) -> float:
    """
    Calculate the variance of a uniform distribution.

    :param a: Lower bound of the distribution.
    :param b: Upper bound of the distribution.
    :return: The variance of the uniform distribution.
    """
    return ((b - a) ** 2) / 12


def calculate_poisson_distribution_mean(lamb: float) -> float:
    """
    Calculate the mean (expected value) of a Poisson distribution.

    :param lamb: The average number of events in an interval.
    :return: The mean of the Poisson distribution.
    """
    return lamb


def calculate_poisson_distribution_variance(lamb: float) -> float:
    """
    Calculate the variance of a Poisson distribution.

    :param lamb: The average number of events in an interval.
    :return: The variance of the Poisson distribution.
    """
    return lamb


def calculate_binomial_probability(n: int, k: int, p: float) -> float:
    """
    Calculate the probability of having exactly k successes in n independent Bernoulli trials
    with probability p of success on each trial, based on the Binomial distribution.

    :param n: Number of trials.
    :param k: Number of successful trials.
    :param p: Probability of success on a single trial.
    :return: The binomial probability of observing exactly k successes.
    """
    return calculate_combination(n, k) * pow(p, k) * pow(1 - p, n - k)


def calculate_geometric_probability(p: float, k: int) -> float:
    """
    Calculate the probability of the first success occurring on the k-th trial in a sequence of Bernoulli trials,
    where each trial has only two possible outcomes (success or failure) and the probability of success is p.

    :param p: The probability of success on a single trial.
    :param k: The trial number of the first success.
    :return: The geometric probability.
    """
    return p * (1 - p) ** (k - 1)


def calculate_geometric_distribution_probability(p: float, x: int) -> float:
    """
    Calculate the probability of the first success occurring on the x-th trial in a series of Bernoulli trials,
    where each trial has a success probability of p.

    :param p: The probability of success on an individual trial.
    :param x: The trial on which the first success occurs.
    :return: The probability of the first success occurring on the x-th trial.
    """
    return pow(1 - p, x - 1) * p


def calculate_poisson_distribution_lambda(events: float, interval: float) -> float:
    """
    Calculate the lambda (λ) parameter for a Poisson distribution.

    This function calculates the lambda (λ) parameter for a Poisson distribution,
    which is the average rate at which events occur in a fixed interval.

    :param events: The average number of events that occur in a fixed interval.
    :param interval: The interval over which the events are measured.
    :return: The lambda (λ) parameter for the Poisson distribution.
    """
    return events / interval


def calculate_negative_binomial_distribution_probability(
    r: int, p: float, x: int
) -> float:
    """
    Calculate the probability of getting the r-th success on the x-th trial in a
    negative binomial distribution.

    This function calculates the probability of observing the r-th success on the
    x-th trial in a sequence of Bernoulli trials with success probability p.

    :param r: The number of successful trials.
    :param p: The probability of success on an individual trial.
    :param x: The trial number on which the r-th success occurs.
    :return: The probability of observing the r-th success on the x-th trial.
    """
    from math import comb

    return comb(x - 1, r - 1) * (p**r) * ((1 - p) ** (x - r))


def calculate_hypergeometric_distribution_probability(
    pop: int, suc: int, n: int, k: int
) -> float:
    """
    Calculate the probability of drawing k successes in n draws from a finite
    population of size pop containing suc successes without replacement.

    This function calculates the probability of drawing k successes in n draws
    from a finite population of size pop containing suc successes, without replacement,
    using the hypergeometric distribution.

    :param pop: The population size.
    :param suc: The number of successes in the population.
    :param n: The number of draws.
    :param k: The number of observed successes.
    :return: The probability of k successes in n draws.
    """
    from math import comb

    return (comb(pop, k) * comb(suc - pop, n - k)) / comb(suc, n)


def calculate_poisson_probability(lambda_: float, k: int) -> float:
    """
    Calculate the probability of observing k events in a fixed interval of time or space,
    given the average number of events (lambda) in that interval.

    :param lambda_: The average number of events in the interval.
    :param k: The number of events observed.
    :return: The Poisson probability.
    """
    from math import exp, factorial

    return (lambda_**k) * exp(-lambda_) / factorial(k)


# statistics


def calculate_variance_sample_or_population(values: list[float], sample: bool) -> float:
    """
    Calculate the variance of a list of numbers.

    :param values: A list of numbers
    :param sample: Boolean indicating if the variance is for a sample (True) or population (False)
    :return: The variance of the numbers
    """
    n = len(values)
    mean_value = calculate_mean(values)
    variance = sum((x - mean_value) ** 2 for x in values) / (n - (1 if sample else 0))
    return variance


def calculate_standard_deviation_sample_or_population(
    values: list[float], sample: bool
) -> float:
    """
    Calculate the standard deviation of a list of numbers.

    :param values: A list of numbers
    :param sample: Boolean indicating if the standard deviation is for a sample (True) or population (False)
    :return: The standard deviation of the numbers
    """
    variance = calculate_variance_sample_or_population(values, sample)
    return variance**0.5


def calculate_population_variance(data: list[float]) -> float:
    """
    Calculate the population variance of a dataset.

    :param data: A list of numerical values representing the dataset.
    :return: The population variance as a float.
    """
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return variance


def calculate_sample_variance(data: list[float]) -> float:
    """
    Calculate the sample variance of a dataset.

    :param data: A list of numerical values representing the dataset.
    :return: The sample variance as a float.
    """
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    return variance


def calculate_population_standard_deviation(data: list[float]) -> float:
    """
    Calculate the population standard deviation of a dataset.

    :param data: A list of numerical values representing the dataset.
    :return: The population standard deviation as a float.
    """
    variance = calculate_population_variance(data)
    return variance**0.5


def calculate_sample_standard_deviation(data: list[float]) -> float:
    """
    Calculate the sample standard deviation of a dataset.

    :param data: A list of numerical values representing the dataset.
    :return: The sample standard deviation as a float.
    """
    variance = calculate_sample_variance(data)
    return variance**0.5


def calculate_mean_absolute_error(actual: list[float], predicted: list[float]) -> float:
    """
    Calculate the mean absolute error (MAE) between actual and predicted values.

    :param actual: A list of actual values.
    :param predicted: A list of predicted values.
    :return: The mean absolute error as a float.
    """
    return sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual)


def calculate_root_mean_square_error(
    actual: list[float], predicted: list[float]
) -> float:
    """
    Calculate the root-mean-square error (RMSE) between actual and predicted values.

    :param actual: A list of actual values.
    :param predicted: A list of predicted values.
    :return: The root-mean-square error as a float.
    """
    return (sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual)) ** 0.5


def calculate_sample_covariance(x: list[float], y: list[float]) -> float:
    """
    Calculate the sample covariance between two lists.

    :param x: A list of values.
    :param y: A list of values.
    :return: The sample covariance as a float.
    """
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    return sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / (n - 1)


def calculate_mean_squared_error(y_true: list[float], y_pred: list[float]) -> float:
    """
    Calculate the mean squared error between true and predicted values.

    :param y_true: List of true values.
    :param y_pred: List of predicted values.
    :return: Mean squared error as a float.
    """
    mse = sum((true - pred) ** 2 for true, pred in zip(y_true, y_pred)) / len(y_true)
    return mse


def calculate_pearson_correlation(x: list[float], y: list[float]) -> float:
    """
    Calculate the Pearson correlation coefficient between two lists.

    :param x: List of x values.
    :param y: List of y values.
    :return: Pearson correlation coefficient as a float.
    """
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(xi**2 for xi in x)
    sum_y2 = sum(yi**2 for yi in y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2)) ** 0.5
    if denominator == 0:
        return 0
    return numerator / denominator


def calculate_root_mean_square(values: list[float]) -> float:
    """
    Calculate the root-mean-square of a list of values.

    :param values: List of values.
    :return: Root-mean-square as a float.
    """
    rms = (sum(value**2 for value in values) / len(values)) ** 0.5
    return rms


def calculate_sample_skewness(data: list[float]) -> float:
    """
    Calculate the sample skewness of a dataset.

    :param data: List of data points.
    :return: Sample skewness as a float.
    """
    n = len(data)
    mean = sum(data) / n
    m3 = sum((xi - mean) ** 3 for xi in data) / n
    m2 = sum((xi - mean) ** 2 for xi in data) / n
    skewness = (n**0.5) * m3 / m2**1.5
    return skewness


def calculate_kurtosis(data: list[float]) -> float:
    """
    Calculate the kurtosis of a dataset.

    :param data: List of data points.
    :return: Kurtosis as a float.
    """
    n = len(data)
    mean = sum(data) / n
    m4 = sum((xi - mean) ** 4 for xi in data) / n
    m2 = sum((xi - mean) ** 2 for xi in data) / n
    kurtosis = (n * m4) / (m2**2) - 3
    return kurtosis


def calculate_z_score(value: float, mean: float, std_dev: float) -> float:
    """
    Calculate the Z-score of a value in a dataset.

    :param value: The value to calculate the Z-score for.
    :param mean: The mean of the dataset.
    :param std_dev: The standard deviation of the dataset.
    :return: The Z-score of the value.
    """
    return (value - mean) / std_dev


def calculate_coefficient_of_variation(data: list[float]) -> float:
    """
    Calculate the coefficient of variation of a dataset.

    :param data: A list of numerical values representing the dataset.
    :return: The coefficient of variation as a float.
    """
    mean = sum(data) / len(data)
    std_dev = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
    return std_dev / mean


def calculate_population_mean(data: list[float]) -> float:
    """
    Calculate the mean (average) of a population data set.

    :param data: A list of numerical values representing the population data.
    :return: The mean of the population data as a float.
    """
    return sum(data) / len(data)


def calculate_sample_standard_error(data: list[float]) -> float:
    """
    Calculate the standard error of a sample data set.

    :param data: A list of numerical values representing the sample data.
    :return: The standard error of the sample data as a float.
    """
    from statistics import stdev

    n = len(data)
    return stdev(data) / n**0.5


def calculate_coefficient_of_determination(
    y_true: list[float], y_pred: list[float]
) -> float:
    """
    Calculate the coefficient of determination (R^2) for a set of true and predicted values.

    :param y_true: A list of true values.
    :param y_pred: A list of predicted values corresponding to the true values.
    :return: The coefficient of determination as a float.
    """
    y_mean = sum(y_true) / len(y_true)
    total_sum_of_squares = sum((yi - y_mean) ** 2 for yi in y_true)
    residual_sum_of_squares = sum((yi - fi) ** 2 for yi, fi in zip(y_true, y_pred))
    return 1 - (residual_sum_of_squares / total_sum_of_squares)


def calculate_population_median(data: list[float]) -> float:
    """
    Calculate the median of a population data set.

    :param data: A list of numerical values representing the population data.
    :return: The median value of the data set.
    """
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 0:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        median = sorted_data[n // 2]
    return median


def calculate_sample_correlation(x: list[float], y: list[float]) -> float:
    """
    Calculate the sample correlation coefficient between two variables.

    :param x: A list of numerical values representing the first variable.
    :param y: A list of numerical values representing the second variable.
    :return: The sample correlation coefficient between x and y.
    """
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum([x[i] * y[i] for i in range(n)])
    sum_x2 = sum([xi**2 for xi in x])
    sum_y2 = sum([yi**2 for yi in y])
    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2)) ** 0.5
    return numerator / denominator


def calculate_population_range(data: list[float]) -> float:
    """
    Calculate the range of a population data set.

    :param data: A list of numerical values representing the population data.
    :return: The range of the population data as a float.
    """
    return max(data) - min(data)


def calculate_sample_proportion(successes: int, trials: int) -> float:
    """
    Calculate the proportion of successes in a sample.

    :param successes: The number of successes in the sample.
    :param trials: The total number of trials or observations in the sample.
    :return: The proportion of successes as a float.
    """
    return successes / trials


def calculate_interquartile_range(data: list[float]) -> float:
    """
    Calculate the interquartile range of a data set.

    :param data: A list of numerical values.
    :return: The interquartile range of the data as a float.
    """
    import numpy as np

    data.sort()
    q3, q1 = np.percentile(data, [75, 25])
    return q3 - q1


def calculate_weighted_mean(values: list[float], weights: list[float]) -> float:
    """
    Calculate the weighted mean of a data set.

    :param values: A list of numerical values.
    :param weights: A list of weights corresponding to the values.
    :return: The weighted mean of the data as a float.
    """
    return sum(value * weight for value, weight in zip(values, weights)) / sum(weights)


if __name__ == "__main__":
    import sys
    from inspect import getmembers, isfunction

    from tulip_agent.function_analyzer import FunctionAnalyzer

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

    fa = FunctionAnalyzer()
    for name, function in functions:
        print(name)
        description = fa.analyze_function(function)
        print(description)

    module_name = "mte"
    too_long = [
        [name, len(module_name + "__" + name)]
        for name, _ in functions
        if len(module_name + "__" + name) > 64
    ]
    if too_long:
        print("Names too long for:")
        c = 0
        for name, ln in too_long:
            print(f"{c} -- {name} -- [{ln}/64]")
            c += 1
