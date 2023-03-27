import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.load_publications import load_overview_workbook
from asc_overview.load_publications.overview_reader.overview_reader import (
    ALL_YEARS,
    OverviewReader,
)
from asc_overview.time_series_tables.outcomes_table.outcomes_table_config import (
    OutcomesRowNames,
)


@pytest.fixture
def overview_reader() -> OverviewReader:
    return OverviewReader(load_overview_workbook())


@pytest.fixture
def outcomes_row_names() -> OutcomesRowNames:
    return params.OUTCOMES_TABLE.ROW_NAMES


def test_get_service_user_quality_of_life(
    overview_reader: OverviewReader, outcomes_row_names: OutcomesRowNames
):
    df_expected = pd.DataFrame(
        {
            outcomes_row_names.SERVICE_USER_QUALITY_OF_LIFE_18_64: [
                19.4,
                19.4,
                19.5,
                19.5,
                19.6,
                19.6,
                19.2,
            ],
            outcomes_row_names.SERVICE_USER_QUALITY_OF_LIFE_65_AND_OVER: [
                18.9,
                18.9,
                18.9,
                18.9,
                18.9,
                18.8,
                18.8,
            ],
        },
        index=[
            "2014-15",
            "2015-16",
            "2016-17",
            "2017-18",
            "2018-19",
            "2019-20",
            "2020-21",
        ],
    )

    df_actual = overview_reader.get_service_user_quality_of_life()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_carer_quality_of_life(
    overview_reader: OverviewReader, outcomes_row_names: OutcomesRowNames
):
    df_expected = pd.DataFrame(
        {
            outcomes_row_names.CARER_QUALITY_OF_LIFE_18_64: [7.6, 7.4, 7.2],
            outcomes_row_names.CARER_QUALITY_OF_LIFE_65_AND_OVER: [8.1, 8.0, 7.8],
        },
        index=["2014-15", "2016-17", "2018-19"],
    )

    df_actual = overview_reader.get_carer_quality_of_life()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_safeguarding_enquiries(
    overview_reader: OverviewReader, outcomes_row_names: OutcomesRowNames
):
    df_expected = pd.DataFrame(
        {
            outcomes_row_names.PERCENT_FULLY_ACHIEVED: [
                67.2,
                67.8,
                68.1,
                66.7,
                68.1,
                68.1,
            ],
            outcomes_row_names.PERCENT_FULLY_OR_PARTLY_ACHIEVED: [
                89.1,
                94.1,
                94.2,
                93.1,
                94.3,
                94.8,
            ],
        },
        index=ALL_YEARS,
    )

    df_actual = overview_reader.get_safeguarding_enquiries()

    pd_testing.assert_frame_equal(df_actual, df_expected)
