"""
Simple Calculator Module
Created by Agent Sigma for multi-agent coordination experiment
Task: task-001-build-calculator
"""


class Calculator:
    """A simple calculator with basic arithmetic operations."""

    def add(self, a, b):
        """Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b
        """
        return a + b

    def subtract(self, a, b):
        """Subtract b from a.

        Args:
            a: First number
            b: Second number

        Returns:
            Difference of a and b
        """
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Product of a and b
        """
        return a * b

    def divide(self, a, b):
        """Divide a by b.

        Args:
            a: Numerator
            b: Denominator

        Returns:
            Quotient of a and b

        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, base, exponent):
        """Raise base to the power of exponent.

        Args:
            base: Base number
            exponent: Exponent

        Returns:
            base raised to exponent
        """
        return base ** exponent

    def modulo(self, a, b):
        """Calculate a modulo b.

        Args:
            a: Dividend
            b: Divisor

        Returns:
            Remainder of a divided by b

        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot calculate modulo with zero divisor")
        return a % b


# Convenience functions for direct use
def add(a, b):
    """Add two numbers."""
    return Calculator().add(a, b)


def subtract(a, b):
    """Subtract b from a."""
    return Calculator().subtract(a, b)


def multiply(a, b):
    """Multiply two numbers."""
    return Calculator().multiply(a, b)


def divide(a, b):
    """Divide a by b."""
    return Calculator().divide(a, b)


def power(base, exponent):
    """Raise base to the power of exponent."""
    return Calculator().power(base, exponent)


def modulo(a, b):
    """Calculate a modulo b."""
    return Calculator().modulo(a, b)


if __name__ == "__main__":
    # Demo usage
    calc = Calculator()
    print("Calculator Demo by Agent Sigma")
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    print(f"15 / 3 = {calc.divide(15, 3)}")
    print(f"2 ^ 8 = {calc.power(2, 8)}")
    print(f"17 % 5 = {calc.modulo(17, 5)}")
