import pandas as pd
import pandas.testing as pd_testing
import pytest
from asc_overview.load_publications.acfr_reader.ascfr_reader import AscfrReader
from asc_overview.load_publications.load_publications import load_ascfr_publication
from asc_overview import params


@pytest.fixture
def ascfr_reader() -> AscfrReader:
    return AscfrReader(load_ascfr_publication())


ASCFR_NUM_COMPLETED_EPISODES_OF_ST_MAX_NEW_CLIENTS_DATA = [
    [
        12235.0,
        30685.0,
        8780.0,
        38905.0,
        7130.0,
        15440.0,
        16460.0,
        5610.0,
        12180.0,
        72040.0,
        219465.0,
    ],
    [
        880.0,
        3120.0,
        790.0,
        4100.0,
        200.0,
        2330.0,
        2105.0,
        945.0,
        2985.0,
        8595.0,
        26060.0,
    ],
    [
        11355.0,
        27565.0,
        7985.0,
        34805.0,
        6925.0,
        13110.0,
        14355.0,
        4665.0,
        9195.0,
        63445.0,
        193405.0,
    ],
]
ASCFR_NUM_COMPLETED_EPISODES_OF_ST_MAX_COLUMN_NAMES = [
    "Early Cessation of Service (not leading to long term support) - 100% NHS funded care/end of life/deceased",
    "Early Cessation of Service (not leading to long term support)",
    "Early Cessation of Service (leading to long term support)",
    "Long Term Support",
    "No Services Provided Needs identified but self funding",
    "Ongoing Low Level Support",
    "Short Term Support",
    "No Services Provided Needs identified but support declined",
    "No Services Provided Universal Services/ signposted to other services",
    "No Services Provided No identified needs",
    "Total",
]


def test_get_new_requests_by_age(ascfr_reader: AscfrReader):
    expected_series = pd.Series(
        data=[
            1710.0,
            577765.0,
            33992830.0,
            12815.0,
            1337875.0,
            10464020.0,
        ],
        index=params.NEW_REQUESTS_TABLE.ASCFR_NEW_INDEX,
        name=params.PUBLICATION_YEAR,
    )

    actual_series = ascfr_reader.get_new_requests_by_age()

    pd_testing.assert_series_equal(expected_series, actual_series)


def test_get_completed_episodes_ST_Max_for_new_clients(
    ascfr_reader: AscfrReader,
):
    df_expected = pd.DataFrame(
        data=ASCFR_NUM_COMPLETED_EPISODES_OF_ST_MAX_NEW_CLIENTS_DATA,
        columns=ASCFR_NUM_COMPLETED_EPISODES_OF_ST_MAX_COLUMN_NAMES,
        index=["All ages", "18-64", "65 and over"],
    )

    df_actual = ascfr_reader.get_completed_episodes_ST_Max_for_new_clients()

    pd_testing.assert_frame_equal(df_expected, df_actual)


def test_get_total_completed_episodes_ST_max_for_existing_clients(
    ascfr_reader: AscfrReader,
):
    df_expected = pd.DataFrame(
        data=[
            [27135.0],
            [3790.0],
            [23345.0],
        ],
        columns=["Total"],
        index=params.SHORT_TERM_CARE_TABLE.COMPLETED_EPISODES_ST_MAX_ROWS,
    )

    df_actual = ascfr_reader.get_total_completed_episodes_ST_Max_for_existing_clients()

    pd_testing.assert_frame_equal(df_expected, df_actual)


def test_get_long_term_support_by_support_setting(ascfr_reader: AscfrReader):
    df_expected = pd.DataFrame(
        [
            [
                7225.0,
                36950.0,
                67605.0,
                25180.0,
                130200.0,
                22325.0,
                55.0,
                150.0,
                289695.0,
            ],
            [
                69160.0,
                140700.0,
                34725.0,
                12240.0,
                264660.0,
                29895.0,
                70.0,
                105.0,
                551550.0,
            ],
        ],
        columns=[
            "Nursing",
            "Residential",
            "Community Direct Payment Only",
            "Community Part Direct Payment",
            "Community CASSR Managed Personal Budget",
            "Community CASSR Commissioned Support Only",
            "Prison CASSR Managed Personal Budget",
            "Prison CASSR Commissioned Support Only",
            "Total",
        ],
        index=["18 to 64", "65 and over"],
    )

    df_actual = ascfr_reader.get_long_term_support_by_support_setting()

    pd_testing.assert_frame_equal(df_expected, df_actual)


def test_get_primary_support_reason_18_64(ascfr_reader: AscfrReader):
    PRIMARY_SUPPORT_REASON_ROW_NAMES = (
        params.LONG_TERM_CARE_TABLE.PRIMARY_SUPPORT_REASON_ROW_NAMES
    )
    expected_series = pd.Series(
        {
            PRIMARY_SUPPORT_REASON_ROW_NAMES.PHYSICAL_SUPP_ACCESS_AND_MOBILITY: 18255,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.PHYSICAL_SUPP_PERSONAL_CARE: 67700,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SENSORY_SUPP_VISUAL: 2065,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SENSORY_SUPP_HEARING: 915,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SENSORY_SUPP_DUAL: 635,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SUPP_WITH_MEMORY_AND_COGNITION: 4905,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.LEARNING_DISABILITY_SUPP: 133670,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.MENTAL_HEALTH_SUPP: 53785,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SOCIAL_SUPP_SUBSTANCE_MISUSE: 980,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SOCIAL_SUPP_ASYLUM: 95,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SOCIAL_SUPP_SOCIAL_ISOLATION: 6680,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = ascfr_reader.get_primary_support_reason_18_64()

    pd_testing.assert_series_equal(expected_series, actual_series)


def test_get_primary_support_reason_65_and_over(ascfr_reader: AscfrReader):
    PRIMARY_SUPPORT_REASON_ROW_NAMES = (
        params.LONG_TERM_CARE_TABLE.PRIMARY_SUPPORT_REASON_ROW_NAMES
    )
    expected_series = pd.Series(
        {
            PRIMARY_SUPPORT_REASON_ROW_NAMES.PHYSICAL_SUPP_ACCESS_AND_MOBILITY: 63565,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.PHYSICAL_SUPP_PERSONAL_CARE: 345005,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SENSORY_SUPP_VISUAL: 4415,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SENSORY_SUPP_HEARING: 1840,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SENSORY_SUPP_DUAL: 1315,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SUPP_WITH_MEMORY_AND_COGNITION: 74040,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.LEARNING_DISABILITY_SUPP: 17895,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.MENTAL_HEALTH_SUPP: 33980,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SOCIAL_SUPP_SUBSTANCE_MISUSE: 490,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SOCIAL_SUPP_ASYLUM: 35,
            PRIMARY_SUPPORT_REASON_ROW_NAMES.SOCIAL_SUPP_SOCIAL_ISOLATION: 8965,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = ascfr_reader.get_primary_support_reason_65_plus()

    pd_testing.assert_series_equal(expected_series, actual_series)


def test_get_real_term_figures(ascfr_reader: AscfrReader):
    expected_index = [
        "2005-06",
        "2006-07",
        "2007-08",
        "2008-09",
        "2009-10",
        "2010-11",
        "2011-12",
        "2012-13",
        "2013-14",
        "2014-15",
        "2015-16",
        "2016-17",
        "2017-18",
        "2018-19",
        "2019-20",
        "2020-21",
    ]
    expected_series = pd.Series(
        [
            20173396.0,
            20331409.0,
            20278586.0,
            20727965.0,
            21335069.0,
            21276166.0,
            21192349.0,
            20689485.0,
            20332327.0,
            19860600.0,
            19653534.0,
            19853602.0,
            19964944.0,
            20464350.0,
            20963833.0,
            21242497.0,
        ],
        index=expected_index,
        name=params.PUBLICATION_YEAR,
    )

    actual_series = ascfr_reader.get_real_term_figures_by_year()

    pd_testing.assert_series_equal(expected_series, actual_series)


def test_get_how_money_spent_figures(ascfr_reader: AscfrReader):
    expected_series = pd.Series(
        {
            "own_provision": 5351104.0,
            "provision_by_others": 20407573.0,
            "grants_voluntary_organisations": 234136.0,
            "total": 25992812.0,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = ascfr_reader.get_how_money_spent_figures_by_measure()

    pd_testing.assert_series_equal(expected_series, actual_series)
