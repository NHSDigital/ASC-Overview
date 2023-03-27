import pytest
import pandas as pd
from asc_overview import params
from asc_overview.load_publications.publications import Publications
from asc_overview.time_series_tables.long_term_care_table.long_term_care_table import (
    calculate_community_care,
    calculate_long_term_support_proportion_by_age,
    calculate_nursing_and_residential,
    calculate_other_primary_support_reason,
    calculate_physical_as_primary_support,
    calculate_total_long_term_support,
    create_new_time_series_column,
    get_population_data_by_age,
)


@pytest.fixture
def long_term_support_by_setting(publications: Publications) -> pd.DataFrame:
    return publications.ascfr.get_long_term_support_by_support_setting()


@pytest.fixture
def primary_support_reason_18_64(publications: Publications) -> pd.Series:
    return publications.ascfr.get_primary_support_reason_18_64()


@pytest.fixture
def primary_support_reason_65_plus(publications: Publications) -> pd.Series:
    return publications.ascfr.get_primary_support_reason_65_plus()


def test_create_new_time_series_column(publications: Publications):
    expected_series = pd.Series(
        [
            289695,
            551550,
            33992831,
            10464019,
            0.009,
            0.053,
            44175,
            245515,
            209860,
            341695,
            85955,
            203730,
            408570,
            142975,
        ],
        index=params.LONG_TERM_CARE_TABLE.get_row_order(),
        name=params.PUBLICATION_YEAR,
    )

    actual_series = create_new_time_series_column(publications)

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore


def test_calculate_total_long_term_support(long_term_support_by_setting: pd.DataFrame):
    expected_series = pd.Series(
        {
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT_18_64: 289695.0,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT_65_PLUS: 551550.0,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = calculate_total_long_term_support(long_term_support_by_setting)

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore


def test_get_population_data_by_age(publications: Publications):
    expected_series = pd.Series(
        {
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.POPULATION_18_64: 33992831,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.POPULATION_65_PLUS: 10464019,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = get_population_data_by_age(publications.ons)

    pd.testing.assert_series_equal(expected_series, actual_series)  # type:ignore


def test_calculate_long_term_support_percentage_by_age(
    long_term_support_by_setting: pd.DataFrame,
):
    input_series = pd.Series(
        {
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.POPULATION_18_64: 33992831,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.POPULATION_65_PLUS: 10464019,
        },
        name=params.PUBLICATION_YEAR,
    )

    expected_series = pd.Series(
        {
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT_PERCENT_18_64: 0.00852224,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT_PERCENT_65_PLUS: 0.05270919,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = calculate_long_term_support_proportion_by_age(
        long_term_support_by_setting, input_series
    )

    pd.testing.assert_series_equal(expected_series, actual_series)  # type:ignore


def test_calculate_nursing_and_residential(long_term_support_by_setting: pd.DataFrame):
    expected_series = pd.Series(
        {
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.NURSING_OR_RESIDENTIAL_18_64: 44175.0,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.NURSING_OR_RESIDENTIAL_65_PLUS: 209860.0,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = calculate_nursing_and_residential(long_term_support_by_setting)

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore


def test_calculate_community_care(long_term_support_by_setting: pd.DataFrame):
    expected_series = pd.Series(
        {
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.COMMUNITY_18_64: 245515.0,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.COMMUNITY_65_PLUS: 341695.0,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = calculate_community_care(long_term_support_by_setting)

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore


def test_calculate_physical_as_primary_support(
    primary_support_reason_18_64: pd.Series, primary_support_reason_65_plus: pd.Series
):
    expected_series = pd.Series(
        {
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.PHYSICAL_SUPPORT_AS_PRIMARY_18_64: 85955,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.PHYSICAL_SUPPORT_AS_PRIMARY_65_PLUS: 408570,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = calculate_physical_as_primary_support(
        primary_support_reason_18_64, primary_support_reason_65_plus
    )

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore


def test_calculate_other_primary_support_reason(
    primary_support_reason_18_64: pd.Series, primary_support_reason_65_plus: pd.Series
):
    expected_series = pd.Series(
        {
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.OTHER_SUPPORT_AS_PRIMARY_18_64: 203730,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.OTHER_SUPPORT_AS_PRIMARY_65_PLUS: 142975,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = calculate_other_primary_support_reason(
        primary_support_reason_18_64, primary_support_reason_65_plus
    )

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore
