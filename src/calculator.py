"""
Simple Calculator Module
Agent: Nexus
Task: task-001
"""


class Calculator:
    """A simple calculator with basic arithmetic operations."""

    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract b from a."""
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        """
        Divide a by b.

        Raises:
            ValueError: If b is zero.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


# Convenience functions
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return Calculator.add(a, b)


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return Calculator.subtract(a, b)


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return Calculator.multiply(a, b)


def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return Calculator.divide(a, b)
