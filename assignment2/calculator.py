import math


class Calculator:
    """
    A simple calculator class that performs basic mathematical operations.
    """

    def add(self, a, b):
        """
        Adds two numbers.

        Parameters:
        - a (float): The first number.
        - b (float): The second number.

        Returns:
        float: The sum of the two numbers.
        """
        return a + b

    def subtract(self, a, b):
        """
        Subtracts the second number from the first.

        Parameters:
        - a (float): The first number.
        - b (float): The second number.

        Returns:
        float: The result of the subtraction.
        """
        return a - b

    def multiply(self, a, b):
        """
        Multiplies two numbers.

        Parameters:
        - a (float): The first number.
        - b (float): The second number.

        Returns:
        float: The product of the two numbers.
        """
        return a * b

    def divide(self, a, b):
        """
        Divides the first number by the second.

        Parameters:
        - a (float): The numerator.
        - b (float): The denominator.

        Returns:
        float: The result of the division.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def square_root(self, a):
        """
        Calculates the square root of a number.

        Parameters:
        - a (float): The number.

        Returns:
        float: The square root of the number.
        """
        if a < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        return math.sqrt(a)

    def power(self, a, b):
        """
        Raises the first number to the power of the second.

        Parameters:
        - a (float): The base.
        - b (float): The exponent.

        Returns:
        float: The result of the exponentiation.
        """
        return a ** b

    def logarithm(self, base, x):
        """
        Calculates the logarithm of a number with a specified base.

        Parameters:
        - base (float): The logarithmic base.
        - x (float): The number.

        Returns:
        float: The result of the logarithmic operation.
        """
        if base <= 0 or base == 1 or x <= 0:
            raise ValueError("Invalid input for logarithmic function")
        return math.log(x, base)

    def sin(self, angle):
        """
        Calculates the sine of an angle in degrees.

        Parameters:
        - angle (float): The angle in degrees.

        Returns:
        float: The sine of the angle.
        """
        return math.sin(math.radians(angle))

    def cos(self, angle):
        """
        Calculates the cosine of an angle in degrees.

        Parameters:
        - angle (float): The angle in degrees.

        Returns:
        float: The cosine of the angle.
        """
        return math.cos(math.radians(angle))

    def tan(self, angle):
        """
        Calculates the tangent of an angle in degrees.

        Parameters:
        - angle (float): The angle in degrees.

        Returns:
        float: The tangent of the angle.
        """
        if abs(angle % 180) == 90:
            raise ValueError("Invalid input for tangent function (cotangent is undefined)")
        return math.tan(math.radians(angle))
