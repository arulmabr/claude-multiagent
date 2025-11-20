"""Data processor module for CSV file operations."""

import csv
from typing import List, Dict, Callable, Any


class DataProcessor:
    """Simple data processing pipeline for CSV files."""

    def __init__(self, filepath: str):
        """Initialize with CSV file path.

        Args:
            filepath: Path to the CSV file
        """
        self.filepath = filepath
        self.data: List[Dict[str, str]] = []

    def load(self) -> 'DataProcessor':
        """Load data from CSV file.

        Returns:
            Self for method chaining
        """
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.data = list(reader)
        return self

    def filter(self, condition: Callable[[Dict[str, str]], bool]) -> 'DataProcessor':
        """Filter data based on condition.

        Args:
            condition: Function that takes a row dict and returns bool

        Returns:
            Self for method chaining
        """
        self.data = [row for row in self.data if condition(row)]
        return self

    def map(self, transform: Callable[[Dict[str, str]], Dict[str, Any]]) -> 'DataProcessor':
        """Transform each row using provided function.

        Args:
            transform: Function that takes a row dict and returns transformed dict

        Returns:
            Self for method chaining
        """
        self.data = [transform(row) for row in self.data]
        return self

    def sort(self, key: str, reverse: bool = False) -> 'DataProcessor':
        """Sort data by specified key.

        Args:
            key: Column name to sort by
            reverse: Sort in descending order if True

        Returns:
            Self for method chaining
        """
        self.data.sort(key=lambda x: x.get(key, ''), reverse=reverse)
        return self

    def get_data(self) -> List[Dict[str, Any]]:
        """Get processed data.

        Returns:
            List of row dictionaries
        """
        return self.data

    def save(self, output_path: str) -> None:
        """Save processed data to CSV file.

        Args:
            output_path: Path for output CSV file
        """
        if not self.data:
            return

        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = self.data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)

    def count(self) -> int:
        """Get count of rows.

        Returns:
            Number of rows in current dataset
        """
        return len(self.data)

    def unique_values(self, column: str) -> List[str]:
        """Get unique values from a column.

        Args:
            column: Column name

        Returns:
            List of unique values
        """
        return list(set(row.get(column, '') for row in self.data))


def quick_filter(input_path: str, output_path: str,
                 condition: Callable[[Dict[str, str]], bool]) -> int:
    """Quick helper to filter CSV file.

    Args:
        input_path: Input CSV file path
        output_path: Output CSV file path
        condition: Filter condition function

    Returns:
        Number of rows after filtering
    """
    processor = DataProcessor(input_path)
    processor.load().filter(condition).save(output_path)
    return processor.count()
