import numpy as np
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.publications import Publications
from asc_overview.time_series_tables.social_care_experience_table.social_care_experience_table import (
    create_new_time_series_column,
)


def test_create_new_time_series_column(publications: Publications):
    expected_series = pd.Series(
        [
            0.699,
            0.661,
            "N/A",
            "N/A",
            np.nan,
            0.650,
            0.260,
            0.077,
            0.013,
            np.nan,
            0.682,
            0.246,
            0.072,
        ],
        index=params.SOCIAL_CARE_EXPERIENCE_TABLE.get_row_order(),
        name=params.PUBLICATION_YEAR,
    )

    actual_series = create_new_time_series_column(publications)

    pd_testing.assert_series_equal(actual_series, expected_series)
