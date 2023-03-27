import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.overview_reader.overview_reader import (
    OverviewReader,
)
from asc_overview.time_series_tables.workforce_table.workforce_table_config import (
    WorkforceRowNames,
)


@pytest.fixture
def workforce_row_names() -> WorkforceRowNames:
    return params.WORKFORCE_TABLE.ROW_NAMES


def test_get_jobs(
    overview_reader: OverviewReader, workforce_row_names: WorkforceRowNames
):
    expected_series = pd.Series(
        {
            "end Sept 2016": 112835,
            "end Sept 2017": 109275,
            "end Sept 2018": 112235,
            "end Sept 2019": 113250,
            "end Sept 2020": 114095,
            "end Sept 2021": 105780,
        },
        name=workforce_row_names.JOBS,
    )

    actual_series = overview_reader.get_jobs()

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_vacancies(
    overview_reader: OverviewReader, workforce_row_names: WorkforceRowNames
):
    expected_series = pd.Series(
        {
            "end Sept 2016": 8230,
            "end Sept 2017": 8790,
            "end Sept 2018": 7160,
            "end Sept 2019": 7405,
            "end Sept 2020": 6585,
            "end Sept 2021": 8035,
        },
        name=workforce_row_names.VACANCIES,
    )

    actual_series = overview_reader.get_vacancies()

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_starters_and_leavers(
    overview_reader: OverviewReader, workforce_row_names: WorkforceRowNames
):
    df_expected = pd.DataFrame(
        {
            workforce_row_names.NEW_STARTERS: [
                13740,
                15150,
                17125,
                15810,
                15290,
                14385,
            ],
            workforce_row_names.LEAVERS: [
                20315,
                19335,
                14255,
                14290,
                13980,
                13320,
            ],
        },
        index=[2016, 2017, 2018, 2019, 2020, 2021],
    )

    df_actual = overview_reader.get_starters_and_leavers()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_job_role(
    overview_reader: OverviewReader, workforce_row_names: WorkforceRowNames
):
    df_expected = pd.DataFrame(
        {
            workforce_row_names.PERCENT_DIRECT_CARE: [
                49.4,
                48.4,
                47.0,
                46.3,
                45.7,
                44.4,
            ],
            workforce_row_names.PERCENT_MANAGER_SUPERVISOR: [
                15.3,
                15.7,
                15.7,
                15.3,
                15.9,
                16.5,
            ],
            workforce_row_names.PERCENT_PROFESSIONAL: [
                17.0,
                17.7,
                18.2,
                18.6,
                18.6,
                18.3,
            ],
            workforce_row_names.PERCENT_OTHER: [
                18.3,
                18.3,
                19.1,
                19.8,
                19.8,
                20.8,
            ],
        },
        index=[
            "end Sept 2016",
            "end Sept 2017",
            "end Sept 2018",
            "end Sept 2019",
            "end Sept 2020",
            "end Sept 2021",
        ],
    )

    df_actual = overview_reader.get_job_role()

    pd_testing.assert_frame_equal(df_actual, df_expected)
