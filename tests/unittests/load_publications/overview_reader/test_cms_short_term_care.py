import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.load_publications import load_overview_workbook
from asc_overview.load_publications.overview_reader.overview_reader import (
    OverviewReader,
    ALL_YEARS,
)
from asc_overview.time_series_tables.short_term_care.short_term_care_table_config import (
    ShortTermCareRowNames,
)


@pytest.fixture
def overview_reader() -> OverviewReader:
    return OverviewReader(load_overview_workbook())


@pytest.fixture
def short_term_care_row_names() -> ShortTermCareRowNames:
    return params.SHORT_TERM_CARE_TABLE.ROW_NAMES


def test_get_short_term_support(
    overview_reader: OverviewReader, short_term_care_row_names: ShortTermCareRowNames
):
    df_expected = pd.DataFrame(
        {
            short_term_care_row_names.TOTAL_COMPLETED_EPISODES_18_64: [
                25995,
                27345,
                29875,
                35880,
                32940,
                29850,
            ],
            short_term_care_row_names.TOTAL_COMPLETED_EPISODES_65_PLUS: [
                221120,
                214470,
                216160,
                219390,
                228665,
                216750,
            ],
        },
        index=ALL_YEARS,
    )

    df_actual = overview_reader.get_short_term_support()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_percent_what_happened_next(
    overview_reader: OverviewReader, short_term_care_row_names: ShortTermCareRowNames
):
    df_expected = pd.DataFrame(
        {
            short_term_care_row_names.PERCENT_EARLY_CESSATION: [
                13.9,
                15.6,
                17.3,
                17.4,
                19.6,
                19.6,
            ],
            short_term_care_row_names.PERCENT_LONG_TERM_SUPPORT: [
                21.0,
                19.0,
                18.8,
                17.7,
                17.7,
                21.7,
            ],
            short_term_care_row_names.PERCENT_ONGOING_LOW_LEVEL_SUPPORT: [
                7.0,
                7.2,
                7.7,
                7.0,
                6.9,
                7.0,
            ],
            short_term_care_row_names.PERCENT_SHORT_TERM_SUPPORT: [
                4.5,
                5.0,
                5.3,
                6.3,
                7.3,
                7.5,
            ],
            short_term_care_row_names.PERCENT_NO_SERVICES_DECLINED: [
                7.4,
                7.2,
                7.8,
                6.2,
                5.9,
                5.8,
            ],
            short_term_care_row_names.PERCENT_NO_SERVICES_UNVERSAL_SIGNPOSTED: [
                8.3,
                9.2,
                10.6,
                6.9,
                7.3,
                5.5,
            ],
            short_term_care_row_names.PERCENT_NO_SERVICES_NO_IDENTIFIED: [
                37.9,
                36.8,
                32.4,
                38.5,
                35.3,
                32.8,
            ],
        },
        index=ALL_YEARS,
    )

    df_actual = overview_reader.get_percent_what_happened_next()

    pd_testing.assert_frame_equal(df_actual, df_expected)
