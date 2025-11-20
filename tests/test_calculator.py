"""
Unit tests for Calculator Module
Created by Agent Sigma for multi-agent coordination experiment
Task: task-001-build-calculator
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from calculator import Calculator, add, subtract, multiply, divide, power, modulo


class TestCalculator(unittest.TestCase):
    """Test cases for Calculator class."""

    def setUp(self):
        """Set up test fixture."""
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        """Test addition of positive numbers."""
        self.assertEqual(self.calc.add(5, 3), 8)
        self.assertEqual(self.calc.add(100, 50), 150)

    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        self.assertEqual(self.calc.add(-5, -3), -8)
        self.assertEqual(self.calc.add(-5, 3), -2)
        self.assertEqual(self.calc.add(5, -3), 2)

    def test_add_zero(self):
        """Test addition with zero."""
        self.assertEqual(self.calc.add(0, 0), 0)
        self.assertEqual(self.calc.add(5, 0), 5)
        self.assertEqual(self.calc.add(0, 5), 5)

    def test_subtract_positive_numbers(self):
        """Test subtraction of positive numbers."""
        self.assertEqual(self.calc.subtract(10, 4), 6)
        self.assertEqual(self.calc.subtract(100, 50), 50)

    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        self.assertEqual(self.calc.subtract(-5, -3), -2)
        self.assertEqual(self.calc.subtract(-5, 3), -8)
        self.assertEqual(self.calc.subtract(5, -3), 8)

    def test_multiply_positive_numbers(self):
        """Test multiplication of positive numbers."""
        self.assertEqual(self.calc.multiply(6, 7), 42)
        self.assertEqual(self.calc.multiply(10, 5), 50)

    def test_multiply_by_zero(self):
        """Test multiplication by zero."""
        self.assertEqual(self.calc.multiply(5, 0), 0)
        self.assertEqual(self.calc.multiply(0, 5), 0)

    def test_multiply_negative_numbers(self):
        """Test multiplication with negative numbers."""
        self.assertEqual(self.calc.multiply(-5, 3), -15)
        self.assertEqual(self.calc.multiply(-5, -3), 15)

    def test_divide_positive_numbers(self):
        """Test division of positive numbers."""
        self.assertEqual(self.calc.divide(15, 3), 5)
        self.assertEqual(self.calc.divide(100, 4), 25)

    def test_divide_with_remainder(self):
        """Test division with decimal result."""
        self.assertAlmostEqual(self.calc.divide(10, 3), 3.333333, places=5)

    def test_divide_by_zero(self):
        """Test that dividing by zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertIn("Cannot divide by zero", str(context.exception))

    def test_power_positive_exponent(self):
        """Test power with positive exponent."""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 2), 25)

    def test_power_zero_exponent(self):
        """Test power with zero exponent."""
        self.assertEqual(self.calc.power(5, 0), 1)

    def test_power_negative_exponent(self):
        """Test power with negative exponent."""
        self.assertEqual(self.calc.power(2, -2), 0.25)

    def test_modulo_positive_numbers(self):
        """Test modulo with positive numbers."""
        self.assertEqual(self.calc.modulo(17, 5), 2)
        self.assertEqual(self.calc.modulo(20, 4), 0)

    def test_modulo_zero_divisor(self):
        """Test that modulo with zero divisor raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.calc.modulo(10, 0)
        self.assertIn("Cannot calculate modulo with zero divisor", str(context.exception))


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""

    def test_add_function(self):
        """Test add convenience function."""
        self.assertEqual(add(5, 3), 8)

    def test_subtract_function(self):
        """Test subtract convenience function."""
        self.assertEqual(subtract(10, 4), 6)

    def test_multiply_function(self):
        """Test multiply convenience function."""
        self.assertEqual(multiply(6, 7), 42)

    def test_divide_function(self):
        """Test divide convenience function."""
        self.assertEqual(divide(15, 3), 5)

    def test_power_function(self):
        """Test power convenience function."""
        self.assertEqual(power(2, 3), 8)

    def test_modulo_function(self):
        """Test modulo convenience function."""
        self.assertEqual(modulo(17, 5), 2)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
