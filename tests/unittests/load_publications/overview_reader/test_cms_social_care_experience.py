import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.load_publications import load_overview_workbook
from asc_overview.load_publications.overview_reader.overview_reader import (
    OverviewReader,
)
from asc_overview.time_series_tables.social_care_experience_table.social_care_experience_table_config import (
    SocialCareExperienceRowNames,
)


@pytest.fixture
def overview_reader() -> OverviewReader:
    return OverviewReader(load_overview_workbook())


@pytest.fixture
def social_care_experience_row_names() -> SocialCareExperienceRowNames:
    return params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES


def test_get_service_user_satisfaction(
    overview_reader: OverviewReader,
    social_care_experience_row_names: SocialCareExperienceRowNames,
):
    df_expected = pd.DataFrame(
        {
            social_care_experience_row_names.SERVICE_USER_SATISFACTION_18_64: [
                68.2,
                68.7,
                68.8,
                68.3,
                68.1,
                68.3,
                69.9,
            ],
            social_care_experience_row_names.SERVICE_USER_SATISFACTION_65_AND_OVER: [
                62.6,
                61.7,
                62.2,
                62.9,
                61.8,
                61.5,
                66.1,
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

    df_actual = overview_reader.get_service_user_satisfaction()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_service_user_feelings_themselves(
    overview_reader: OverviewReader,
    social_care_experience_row_names: SocialCareExperienceRowNames,
):
    df_expected = pd.DataFrame(
        {
            social_care_experience_row_names.FEEL_BETTER_ABOUT_SELF: [
                61.3,
                62.4,
                62.3,
                62.5,
                62.0,
                62.0,
                65.0,
            ],
            social_care_experience_row_names.DOES_NOT_AFFECT_SELF: [
                29.8,
                29.0,
                29.0,
                28.5,
                28.6,
                28.4,
                26.0,
            ],
            social_care_experience_row_names.SOMETIMES_UNDERMINES_SELF: [
                7.6,
                7.5,
                7.7,
                7.8,
                8.1,
                8.2,
                7.7,
            ],
            social_care_experience_row_names.COMPLETELY_UNDERMINES_SELF: [
                1.2,
                1.1,
                1.1,
                1.2,
                1.2,
                1.4,
                1.3,
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

    df_actual = overview_reader.get_service_user_feelings_themselves()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_service_user_feelings_choice(
    overview_reader: OverviewReader,
    social_care_experience_row_names: SocialCareExperienceRowNames,
):
    df_expected = pd.DataFrame(
        {
            social_care_experience_row_names.HAVE_ENOUGH_CHOICE: [
                68.2,
                68.2,
                67.5,
                66.6,
                68.2,
            ],
            social_care_experience_row_names.DONT_HAVE_ENOUGH_CHOICE: [
                25.8,
                25.8,
                26.9,
                27.9,
                24.6,
            ],
            social_care_experience_row_names.DONT_WANT_CHOICE: [
                6.0,
                6.0,
                5.7,
                5.5,
                7.2,
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

    df_actual = overview_reader.get_service_user_feelings_choice()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_carer_satisfaction(
    overview_reader: OverviewReader,
    social_care_experience_row_names: SocialCareExperienceRowNames,
):
    df_expected = pd.DataFrame(
        {
            social_care_experience_row_names.CARER_SATISFACTION_18_64: [
                38.8,
                36.3,
                36.1,
            ],
            social_care_experience_row_names.CARER_SATISFACTION_65_AND_OVER: [
                43.6,
                41.3,
                41.0,
            ],
        },
        index=["2014-15", "2016-17", "2018-19"],
    )

    df_actual = overview_reader.get_carer_satisfaction()

    pd_testing.assert_frame_equal(df_actual, df_expected)
