"""
Unit tests for Calculator Module
Agent: Nexus
Task: task-001
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator import Calculator, add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):
    """Test cases for Calculator class."""

    def test_add(self):
        """Test addition."""
        self.assertEqual(Calculator.add(2, 3), 5)
        self.assertEqual(Calculator.add(-1, 1), 0)
        self.assertEqual(Calculator.add(0, 0), 0)
        self.assertEqual(Calculator.add(1.5, 2.5), 4.0)

    def test_subtract(self):
        """Test subtraction."""
        self.assertEqual(Calculator.subtract(5, 3), 2)
        self.assertEqual(Calculator.subtract(1, 1), 0)
        self.assertEqual(Calculator.subtract(0, 5), -5)
        self.assertEqual(Calculator.subtract(2.5, 1.5), 1.0)

    def test_multiply(self):
        """Test multiplication."""
        self.assertEqual(Calculator.multiply(2, 3), 6)
        self.assertEqual(Calculator.multiply(-2, 3), -6)
        self.assertEqual(Calculator.multiply(0, 100), 0)
        self.assertEqual(Calculator.multiply(2.5, 2), 5.0)

    def test_divide(self):
        """Test division."""
        self.assertEqual(Calculator.divide(6, 2), 3)
        self.assertEqual(Calculator.divide(5, 2), 2.5)
        self.assertEqual(Calculator.divide(-10, 2), -5)

    def test_divide_by_zero(self):
        """Test that dividing by zero raises ValueError."""
        with self.assertRaises(ValueError):
            Calculator.divide(5, 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""

    def test_add_function(self):
        """Test add convenience function."""
        self.assertEqual(add(2, 3), 5)

    def test_subtract_function(self):
        """Test subtract convenience function."""
        self.assertEqual(subtract(5, 3), 2)

    def test_multiply_function(self):
        """Test multiply convenience function."""
        self.assertEqual(multiply(2, 3), 6)

    def test_divide_function(self):
        """Test divide convenience function."""
        self.assertEqual(divide(6, 2), 3)

    def test_divide_function_zero(self):
        """Test divide convenience function with zero."""
        with self.assertRaises(ValueError):
            divide(5, 0)


if __name__ == '__main__':
    unittest.main()
