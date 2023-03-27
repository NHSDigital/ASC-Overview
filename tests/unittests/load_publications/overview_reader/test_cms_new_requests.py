import pytest
import numpy as np
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.load_publications import load_overview_workbook
from asc_overview.load_publications.overview_reader.overview_reader import (
    OverviewReader,
    ALL_YEARS,
)
from asc_overview.time_series_tables.new_requests_table.new_requests_table_config import (
    NewRequestsRowNames,
)


@pytest.fixture
def overview_reader() -> OverviewReader:
    return OverviewReader(load_overview_workbook())


@pytest.fixture
def new_requests_row_names() -> NewRequestsRowNames:
    return params.NEW_REQUESTS_TABLE.ROW_NAMES


def test_get_new_requests_for_support(
    overview_reader: OverviewReader, new_requests_row_names: NewRequestsRowNames
):
    df_expected = pd.DataFrame(
        {
            new_requests_row_names.ASCFR_NEW_REQUESTS_18_64_NAME: [
                500670,
                508620,
                523920,
                550435,
                560350,
                577765,
            ],
            new_requests_row_names.ASCFR_NEW_REQUESTS_65_PLUS_NAME: [
                1310060,
                1305795,
                1320000,
                1364095,
                1370205,
                1337875,
            ],
        },
        index=ALL_YEARS,
    )

    df_actual = overview_reader.get_new_requests_for_support()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_change_in_requests(
    overview_reader: OverviewReader, new_requests_row_names: NewRequestsRowNames
):
    df_expected = pd.DataFrame(
        {
            new_requests_row_names.ASCFR_GROWTH_18_64_SINCE_2015_16_NAME: [
                0.016,
                0.046,
                0.099,
                0.119,
                0.154,
            ],
            new_requests_row_names.ASCFR_GROWTH_65_PLUS_SINCE_2015_16_NAME: [
                -0.003,
                0.008,
                0.041,
                0.046,
                0.021,
            ],
        },
        index=[
            "2016-17",
            "2017-18",
            "2018-19",
            "2019-20",
            "2020-21",
        ],
    )

    df_actual = overview_reader.get_change_in_requests()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_new_requests_per_population(
    overview_reader: OverviewReader, new_requests_row_names: NewRequestsRowNames
):
    df_expected = pd.DataFrame(
        {
            new_requests_row_names.NEW_REQUESTS_PER_POPULATION_18_64: [
                1499,
                1514,
                1554,
                1626,
                1652,
                1710,
            ],
            new_requests_row_names.NEW_REQUESTS_PER_POPULATION_65_PLUS: [
                13490,
                13213,
                13160,
                13401,
                13234,
                12815,
            ],
        },
        index=ALL_YEARS,
    )

    df_actual = overview_reader.get_new_requests_per_population()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_dols_requests(
    overview_reader: OverviewReader, new_requests_row_names: NewRequestsRowNames
):
    expected_series = pd.Series(
        {
            "2015-16": 195840,
            "2016-17": 217235,
            "2017-18": 227400,
            "2018-19": 240455,
            "2019-20": 263940,
            "2020-21": 256610,
        },
        name=new_requests_row_names.DOLS_APPLICATIONS_RECEIVED_NAME,
    )

    actual_series = overview_reader.get_dols_requests()

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_safeguarding_requests(
    overview_reader: OverviewReader, new_requests_row_names: NewRequestsRowNames
):
    expected_series = pd.Series(
        {
            "2016-17": 364605,
            "2017-18": 394655,
            "2018-19": 415050,
            "2019-20": 475560,
            "2020-21": 498260,
        },
        name=new_requests_row_names.SAFEGUARDING_CONCERNS_RAISED_NAME,
    )

    actual_series = overview_reader.get_safeguarding_requests()

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_change_in_safeguarding_and_dols(
    overview_reader: OverviewReader, new_requests_row_names: NewRequestsRowNames
):
    df_expected = pd.DataFrame(
        {
            new_requests_row_names.SAFEGUARDING_YEAR_ON_YEAR_CONCERNS_RAISED_NAME: [
                np.nan,
                0.082,
                0.052,
                0.146,
                0.048,
            ],
            new_requests_row_names.DOLS_YEAR_ON_YEAR_APPLICATIONS_RECEIVED_NAME: [
                0.109,
                0.047,
                0.057,
                0.098,
                -0.028,
            ],
        },
        index=[
            "2016-17",
            "2017-18",
            "2018-19",
            "2019-20",
            "2020-21",
        ],
    )

    df_actual = overview_reader.get_change_in_safeguarding_and_dols()

    pd_testing.assert_frame_equal(df_actual, df_expected)
