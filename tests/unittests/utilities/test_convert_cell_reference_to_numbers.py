import pytest
from asc_overview.utilities.convert_cell_ref_to_numbers import (
    convert_cell_ref_to_numbers_one_based,
    convert_cell_ref_to_numbers_zero_based,
)


@pytest.mark.parametrize(
    "cell_ref,expected_column_start,expected_row_start",
    [
        ("A1", 0, 0),
        ("B2", 1, 1),
        ("C3", 2, 2),
        ("A7", 0, 6),
        ("Q4", 16, 3),
        ("AA1", 26, 0),
        ("AB1", 27, 0),
        ("AZ1", 51, 0),
        ("BA1", 52, 0),
        ("ZZ1", 701, 0),
        ("AAA1", 702, 0),
        ("BBZ1", 1429, 0),
    ],
)
def test_convert_cell_ref_to_numbers(
    cell_ref: str, expected_column_start: int, expected_row_start: int
):

    column_start, row_start = convert_cell_ref_to_numbers_zero_based(cell_ref)

    assert column_start == expected_column_start
    assert row_start == expected_row_start
