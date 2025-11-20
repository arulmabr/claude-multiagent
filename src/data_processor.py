"""
Data Processor Module
A simple CSV data processing pipeline with filtering and output capabilities.
Created by: Agent Sonnet
Task: task-002
"""

import csv
from typing import List, Dict, Any, Callable, Optional
from pathlib import Path


class DataProcessor:
    """Process CSV data with filtering and transformation capabilities."""

    def __init__(self, filepath: str):
        """
        Initialize the data processor with a CSV file.

        Args:
            filepath: Path to the CSV file to process
        """
        self.filepath = Path(filepath)
        self.data: List[Dict[str, Any]] = []
        self.filtered_data: List[Dict[str, Any]] = []

    def load(self) -> 'DataProcessor':
        """
        Load data from the CSV file.

        Returns:
            Self for method chaining
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")

        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.data = list(reader)
            self.filtered_data = self.data.copy()

        return self

    def filter(self, condition: Callable[[Dict[str, Any]], bool]) -> 'DataProcessor':
        """
        Filter data based on a condition function.

        Args:
            condition: Function that takes a row dict and returns True to keep it

        Returns:
            Self for method chaining
        """
        self.filtered_data = [row for row in self.filtered_data if condition(row)]
        return self

    def filter_by_column(self, column: str, value: Any) -> 'DataProcessor':
        """
        Filter data where column equals value.

        Args:
            column: Column name to filter on
            value: Value to match (exact match)

        Returns:
            Self for method chaining
        """
        return self.filter(lambda row: row.get(column) == str(value))

    def filter_range(self, column: str, min_val: float, max_val: float) -> 'DataProcessor':
        """
        Filter numeric data within a range.

        Args:
            column: Column name containing numeric data
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)

        Returns:
            Self for method chaining
        """
        def in_range(row: Dict[str, Any]) -> bool:
            try:
                val = float(row.get(column, 0))
                return min_val <= val <= max_val
            except (ValueError, TypeError):
                return False

        return self.filter(in_range)

    def sort(self, column: str, reverse: bool = False) -> 'DataProcessor':
        """
        Sort filtered data by column.

        Args:
            column: Column name to sort by
            reverse: If True, sort descending

        Returns:
            Self for method chaining
        """
        self.filtered_data.sort(key=lambda row: row.get(column, ''), reverse=reverse)
        return self

    def get_results(self) -> List[Dict[str, Any]]:
        """
        Get the filtered results.

        Returns:
            List of filtered row dictionaries
        """
        return self.filtered_data

    def count(self) -> int:
        """
        Count filtered results.

        Returns:
            Number of rows in filtered data
        """
        return len(self.filtered_data)

    def save(self, output_path: str, columns: Optional[List[str]] = None) -> 'DataProcessor':
        """
        Save filtered results to a CSV file.

        Args:
            output_path: Path for output CSV file
            columns: Optional list of columns to include (defaults to all)

        Returns:
            Self for method chaining
        """
        if not self.filtered_data:
            # Create empty file if no data
            Path(output_path).touch()
            return self

        # Determine columns to write
        if columns is None:
            columns = list(self.filtered_data[0].keys())

        # Filter rows to only include specified columns
        filtered_rows = [{col: row.get(col, '') for col in columns} for row in self.filtered_data]

        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(filtered_rows)

        return self

    def summary(self) -> Dict[str, Any]:
        """
        Get summary statistics about the data.

        Returns:
            Dictionary with summary information
        """
        return {
            'total_rows': len(self.data),
            'filtered_rows': len(self.filtered_data),
            'columns': list(self.data[0].keys()) if self.data else [],
            'filter_percentage': (len(self.filtered_data) / len(self.data) * 100) if self.data else 0
        }

    def reset(self) -> 'DataProcessor':
        """
        Reset filtered data to original loaded data.

        Returns:
            Self for method chaining
        """
        self.filtered_data = self.data.copy()
        return self


def process_csv(filepath: str,
                filter_fn: Optional[Callable] = None,
                output_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Convenience function to process a CSV file in one call.

    Args:
        filepath: Input CSV file path
        filter_fn: Optional filter function
        output_path: Optional output CSV file path

    Returns:
        List of processed row dictionaries
    """
    processor = DataProcessor(filepath).load()

    if filter_fn:
        processor.filter(filter_fn)

    if output_path:
        processor.save(output_path)

    return processor.get_results()
