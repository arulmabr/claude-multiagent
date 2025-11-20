"""Tests for data_processor module."""

import os
import sys
import tempfile
import csv

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processor import DataProcessor, quick_filter


def test_load():
    """Test loading CSV data."""
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.csv')
    processor = DataProcessor(sample_path)
    processor.load()

    assert processor.count() == 10, f"Expected 10 rows, got {processor.count()}"
    assert len(processor.get_data()) == 10


def test_filter():
    """Test filtering data."""
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.csv')
    processor = DataProcessor(sample_path)

    # Filter for Engineering department
    processor.load().filter(lambda row: row['department'] == 'Engineering')

    assert processor.count() == 4, f"Expected 4 engineers, got {processor.count()}"


def test_filter_by_age():
    """Test filtering by numeric condition."""
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.csv')
    processor = DataProcessor(sample_path)

    # Filter for age > 30
    processor.load().filter(lambda row: int(row['age']) > 30)

    assert processor.count() == 5, f"Expected 5 people over 30, got {processor.count()}"


def test_filter_by_salary():
    """Test filtering by salary."""
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.csv')
    processor = DataProcessor(sample_path)

    # Filter for salary >= 100000
    processor.load().filter(lambda row: int(row['salary']) >= 100000)

    assert processor.count() == 4, f"Expected 4 high earners, got {processor.count()}"


def test_chaining():
    """Test method chaining."""
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.csv')
    processor = DataProcessor(sample_path)

    # Chain: load -> filter department -> filter age
    result = (processor.load()
              .filter(lambda row: row['department'] == 'Engineering')
              .filter(lambda row: int(row['age']) > 30)
              .get_data())

    assert len(result) == 3, f"Expected 3 senior engineers, got {len(result)}"


def test_map():
    """Test data transformation."""
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.csv')
    processor = DataProcessor(sample_path)

    # Add computed field
    processor.load().map(lambda row: {
        **row,
        'salary_k': str(int(row['salary']) // 1000) + 'k'
    })

    data = processor.get_data()
    assert 'salary_k' in data[0], "Expected salary_k field to be added"


def test_sort():
    """Test sorting data."""
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.csv')
    processor = DataProcessor(sample_path)

    processor.load().sort('age', reverse=True)
    data = processor.get_data()

    # First should be oldest (45)
    assert int(data[0]['age']) == 45, f"Expected oldest first, got age {data[0]['age']}"


def test_unique_values():
    """Test getting unique values."""
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.csv')
    processor = DataProcessor(sample_path)

    processor.load()
    departments = processor.unique_values('department')

    assert len(departments) == 4, f"Expected 4 departments, got {len(departments)}"
    assert 'Engineering' in departments


def test_save():
    """Test saving processed data."""
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.csv')

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        output_path = tmp.name

    try:
        processor = DataProcessor(sample_path)
        processor.load().filter(lambda row: row['department'] == 'Engineering').save(output_path)

        # Verify output file
        with open(output_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 4, f"Expected 4 rows in output, got {len(rows)}"

    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


def test_quick_filter():
    """Test quick_filter helper function."""
    sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.csv')

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        output_path = tmp.name

    try:
        count = quick_filter(sample_path, output_path,
                            lambda row: int(row['salary']) >= 100000)

        assert count == 4, f"Expected 4 rows, got {count}"
        assert os.path.exists(output_path), "Output file should exist"

    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        ("Load data", test_load),
        ("Filter by department", test_filter),
        ("Filter by age", test_filter_by_age),
        ("Filter by salary", test_filter_by_salary),
        ("Method chaining", test_chaining),
        ("Map transformation", test_map),
        ("Sort data", test_sort),
        ("Unique values", test_unique_values),
        ("Save to file", test_save),
        ("Quick filter", test_quick_filter),
    ]

    passed = 0
    failed = 0

    print("Running data_processor tests...\n")

    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {name}: Unexpected error: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed, {passed + failed} total")
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
