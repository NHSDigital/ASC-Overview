import re
from typing import NamedTuple


class CellReferenceNumbers(NamedTuple):
    column: int
    row: int


def convert_cell_ref_to_numbers_one_based(
    cell_ref: str,
) -> CellReferenceNumbers:
    column_as_letters, row_number = re.match(r"([a-zA-Z]+)(\d+)", cell_ref).groups()

    column_start = 0
    for i, char in enumerate(column_as_letters):
        base_26_exponent = len(column_as_letters) - i - 1
        column_start += 26**base_26_exponent
        column_start += (ord(char.lower()) - 97) * 26**base_26_exponent

    row_start = int(row_number)

    return CellReferenceNumbers(column=column_start, row=row_start)


def convert_cell_ref_to_numbers_zero_based(
    cell_ref: str,
) -> CellReferenceNumbers:
    cell_ref_as_numbers_one_based = convert_cell_ref_to_numbers_one_based(cell_ref)

    return CellReferenceNumbers(
        column=cell_ref_as_numbers_one_based.column - 1,
        row=cell_ref_as_numbers_one_based.row - 1,
    )
