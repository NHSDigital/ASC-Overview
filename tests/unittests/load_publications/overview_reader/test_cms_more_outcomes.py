import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.load_publications import load_overview_workbook
from asc_overview.load_publications.overview_reader.overview_reader import (
    OverviewReader,
)
from asc_overview.time_series_tables.more_outcomes_table.more_outcomes_table_config import (
    MoreOutcomesRowNames,
)


@pytest.fixture
def overview_reader() -> OverviewReader:
    return OverviewReader(load_overview_workbook())


@pytest.fixture
def more_outcomes_row_names() -> MoreOutcomesRowNames:
    return params.MORE_OUTCOMES_TABLE.ROW_NAMES


def test_get_service_user_feelings_safety(
    overview_reader: OverviewReader, more_outcomes_row_names: MoreOutcomesRowNames
):
    df_expected = pd.DataFrame(
        {
            more_outcomes_row_names.SERVICE_USER_SAFETY_18_64: [
                65.8,
                66.7,
                67.8,
                68.3,
                68.3,
                68.6,
                70.9,
            ],
            more_outcomes_row_names.SERVICE_USER_SAFETY_65_AND_OVER: [
                70.2,
                70.7,
                71.4,
                70.9,
                71.2,
                71.2,
                75.6,
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

    df_actual = overview_reader.get_service_user_feelings_safety()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_service_user_social_contact(
    overview_reader: OverviewReader, more_outcomes_row_names: MoreOutcomesRowNames
):
    df_expected = pd.DataFrame(
        {
            more_outcomes_row_names.SERVICE_USER_SOCIAL_CONTACT_18_64: [
                48.0,
                48.2,
                49.0,
                49.2,
                49.6,
                49.8,
                36.8,
            ],
            more_outcomes_row_names.SERVICE_USER_SOCIAL_CONTACT_65_AND_OVER: [
                42.8,
                43.7,
                43.2,
                44.0,
                43.5,
                43.4,
                32.7,
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

    df_actual = overview_reader.get_service_user_social_contact()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_carer_social_contact(
    overview_reader: OverviewReader, more_outcomes_row_names: MoreOutcomesRowNames
):
    df_expected = pd.DataFrame(
        {
            more_outcomes_row_names.CARERS_SOCIAL_CONTACT_18_64: [36.3, 32.3, 29.5],
            more_outcomes_row_names.CARERS_SOCIAL_CONTACT_65_AND_OVER: [
                40.0,
                38.3,
                34.5,
            ],
        },
        index=["2014-15", "2016-17", "2018-19"],
    )

    df_actual = overview_reader.get_carer_social_contact()

    pd_testing.assert_frame_equal(df_actual, df_expected)
