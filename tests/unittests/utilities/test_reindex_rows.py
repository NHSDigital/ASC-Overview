import numpy as np
import pandas as pd
import pandas.testing as pd_testing
import pytest
from asc_overview.utilities.reindex_rows import (
    reindex_rows,
    check_no_rows_will_be_lost_on_reindex,
)


def test_reindex_rows():
    input_series = pd.Series({"ROW_2": "b", "ROW_1": "a"})
    row_order = ["ROW_1", "ROW_2", "ROW_3"]

    expected_series = pd.Series({"ROW_1": "a", "ROW_2": "b", "ROW_3": np.nan})

    actual_series = reindex_rows(input_series, row_order)

    pd_testing.assert_series_equal(expected_series, actual_series)


def test_check_no_rows_will_be_lost_on_reindex_raises_error():
    index_before_reindex = pd.Index(["index_1", "index_2", "index_3", "index_4"])
    index_after_reindex = pd.Index(["index_1", "index_2", "index_3"])

    with pytest.raises(AssertionError) as err:
        check_no_rows_will_be_lost_on_reindex(index_before_reindex, index_after_reindex)

    assert "index_4" in str(err.value)
