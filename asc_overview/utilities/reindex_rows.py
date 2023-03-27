import pandas as pd
from typed_params import BaseModel


def get_row_order_from_row_names(row_names: BaseModel):
    return list(row_names.to_dict().values())


def reindex_rows(new_time_series_column: pd.Series, row_order: list[str]) -> pd.Series:
    index_before_reindex = new_time_series_column.index
    index_after_reindex = pd.Index(row_order)

    check_no_rows_will_be_lost_on_reindex(index_before_reindex, index_after_reindex)

    return new_time_series_column.reindex(index_after_reindex).loc[row_order]


def check_no_rows_will_be_lost_on_reindex(
    index_before_reindex: pd.Index, index_after_reindex: pd.Index
):
    overlapping_rows = index_before_reindex.intersection(index_after_reindex)
    elements_that_have_been_lost = index_before_reindex.difference(overlapping_rows)

    assert (
        len(elements_that_have_been_lost) == 0
    ), f"""
    Reindexing to add missing rows would remove rows.
    This likely indicates that params.py is wrong somehow.
    The elements that have been lost are:
    {elements_that_have_been_lost}
    """
