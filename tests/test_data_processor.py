"""
Tests for Data Processor Module
Created by: Agent Sonnet
Task: task-002
"""

import pytest
import csv
import tempfile
from pathlib import Path
from src.data_processor import DataProcessor, process_csv


class TestDataProcessor:
    """Test suite for DataProcessor class."""

    @pytest.fixture
    def sample_csv(self):
        """Create a temporary CSV file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name', 'age', 'score'])
            writer.writeheader()
            writer.writerows([
                {'id': '1', 'name': 'Alice', 'age': '25', 'score': '85'},
                {'id': '2', 'name': 'Bob', 'age': '30', 'score': '92'},
                {'id': '3', 'name': 'Carol', 'age': '28', 'score': '78'},
                {'id': '4', 'name': 'David', 'age': '35', 'score': '95'},
                {'id': '5', 'name': 'Eve', 'age': '22', 'score': '88'},
            ])
            temp_path = f.name

        yield temp_path

        # Cleanup
        Path(temp_path).unlink(missing_ok=True)

    def test_load_data(self, sample_csv):
        """Test loading data from CSV file."""
        processor = DataProcessor(sample_csv).load()
        assert len(processor.data) == 5
        assert processor.data[0]['name'] == 'Alice'
        assert processor.data[0]['age'] == '25'

    def test_load_nonexistent_file(self):
        """Test loading a file that doesn't exist."""
        processor = DataProcessor('nonexistent.csv')
        with pytest.raises(FileNotFoundError):
            processor.load()

    def test_filter_by_column(self, sample_csv):
        """Test filtering by exact column value."""
        processor = DataProcessor(sample_csv).load()
        processor.filter_by_column('name', 'Alice')
        results = processor.get_results()

        assert len(results) == 1
        assert results[0]['name'] == 'Alice'
        assert results[0]['age'] == '25'

    def test_filter_custom_condition(self, sample_csv):
        """Test filtering with custom condition function."""
        processor = DataProcessor(sample_csv).load()
        processor.filter(lambda row: int(row['age']) >= 30)
        results = processor.get_results()

        assert len(results) == 2
        assert all(int(row['age']) >= 30 for row in results)

    def test_filter_range(self, sample_csv):
        """Test filtering numeric values within a range."""
        processor = DataProcessor(sample_csv).load()
        processor.filter_range('score', 85, 92)
        results = processor.get_results()

        assert len(results) == 3
        scores = [float(row['score']) for row in results]
        assert all(85 <= score <= 92 for score in scores)

    def test_chained_filters(self, sample_csv):
        """Test chaining multiple filters."""
        processor = DataProcessor(sample_csv).load()
        processor.filter_range('age', 25, 30).filter_range('score', 80, 95)
        results = processor.get_results()

        assert len(results) == 2
        for row in results:
            assert 25 <= int(row['age']) <= 30
            assert 80 <= int(row['score']) <= 95

    def test_sort_ascending(self, sample_csv):
        """Test sorting data in ascending order."""
        processor = DataProcessor(sample_csv).load()
        processor.sort('age')
        results = processor.get_results()

        ages = [int(row['age']) for row in results]
        assert ages == sorted(ages)
        assert results[0]['name'] == 'Eve'  # Youngest

    def test_sort_descending(self, sample_csv):
        """Test sorting data in descending order."""
        processor = DataProcessor(sample_csv).load()
        processor.sort('score', reverse=True)
        results = processor.get_results()

        scores = [int(row['score']) for row in results]
        assert scores == sorted(scores, reverse=True)
        assert results[0]['name'] == 'David'  # Highest score

    def test_count(self, sample_csv):
        """Test counting filtered results."""
        processor = DataProcessor(sample_csv).load()
        assert processor.count() == 5

        processor.filter_by_column('name', 'Alice')
        assert processor.count() == 1

        processor.reset().filter_range('age', 20, 25)
        assert processor.count() == 2

    def test_reset(self, sample_csv):
        """Test resetting filtered data."""
        processor = DataProcessor(sample_csv).load()
        processor.filter_by_column('name', 'Alice')
        assert processor.count() == 1

        processor.reset()
        assert processor.count() == 5

    def test_save(self, sample_csv):
        """Test saving filtered results to file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_path = f.name

        try:
            processor = DataProcessor(sample_csv).load()
            processor.filter_range('age', 25, 30).save(output_path)

            # Verify saved file
            with open(output_path, 'r') as f:
                reader = csv.DictReader(f)
                saved_data = list(reader)

            assert len(saved_data) == 3
            assert saved_data[0]['name'] == 'Alice'

        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_save_with_columns(self, sample_csv):
        """Test saving only specific columns."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_path = f.name

        try:
            processor = DataProcessor(sample_csv).load()
            processor.save(output_path, columns=['name', 'score'])

            # Verify saved file has only specified columns
            with open(output_path, 'r') as f:
                reader = csv.DictReader(f)
                saved_data = list(reader)

            assert list(saved_data[0].keys()) == ['name', 'score']
            assert 'age' not in saved_data[0]

        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_save_empty_results(self, sample_csv):
        """Test saving when no results match filter."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_path = f.name

        try:
            processor = DataProcessor(sample_csv).load()
            processor.filter_by_column('name', 'NonexistentName').save(output_path)

            # Verify empty file was created
            assert Path(output_path).exists()
            assert Path(output_path).stat().st_size == 0

        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_summary(self, sample_csv):
        """Test getting summary statistics."""
        processor = DataProcessor(sample_csv).load()
        summary = processor.summary()

        assert summary['total_rows'] == 5
        assert summary['filtered_rows'] == 5
        assert 'name' in summary['columns']
        assert summary['filter_percentage'] == 100.0

        processor.filter_by_column('name', 'Alice')
        summary = processor.summary()

        assert summary['total_rows'] == 5
        assert summary['filtered_rows'] == 1
        assert summary['filter_percentage'] == 20.0

    def test_method_chaining(self, sample_csv):
        """Test fluent interface with method chaining."""
        results = (DataProcessor(sample_csv)
                   .load()
                   .filter_range('age', 25, 35)
                   .filter_range('score', 85, 95)
                   .sort('score', reverse=True)
                   .get_results())

        assert len(results) > 0
        assert isinstance(results, list)

    def test_process_csv_convenience_function(self, sample_csv):
        """Test the convenience function."""
        results = process_csv(sample_csv, lambda row: int(row['age']) >= 30)

        assert len(results) == 2
        assert all(int(row['age']) >= 30 for row in results)

    def test_process_csv_with_output(self, sample_csv):
        """Test convenience function with output file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_path = f.name

        try:
            results = process_csv(
                sample_csv,
                lambda row: int(row['score']) >= 85,
                output_path
            )

            assert len(results) == 4
            assert Path(output_path).exists()

        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_real_world_sample(self):
        """Test with the actual sample.csv file if it exists."""
        sample_path = Path('data/sample.csv')
        if not sample_path.exists():
            pytest.skip("data/sample.csv not found")

        processor = DataProcessor('data/sample.csv').load()

        # Test filtering engineers
        engineers = processor.filter_by_column('department', 'Engineering').get_results()
        assert len(engineers) > 0
        assert all(row['department'] == 'Engineering' for row in engineers)

        # Test salary range filtering
        processor.reset()
        high_earners = processor.filter_range('salary', 80000, 100000).get_results()
        assert len(high_earners) > 0

        # Test complex query
        processor.reset()
        senior_engineers = (processor
                           .filter_by_column('department', 'Engineering')
                           .filter_range('years_experience', 10, 25)
                           .sort('salary', reverse=True)
                           .get_results())

        assert isinstance(senior_engineers, list)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
