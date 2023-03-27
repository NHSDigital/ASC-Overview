import pytest
import pandas as pd
import numpy as np
from asc_overview import params
from asc_overview.load_publications.publications import Publications
from asc_overview.time_series_tables.short_term_care.short_term_care_table import (
    calculate_measure_percentages,
    calculate_measures,
    calculate_total_completed_episodes_of_ST_Max,
    create_new_time_series_column,
    create_what_happened_next_series,
    create_series_from_sum_of_completed_episodes_columns,
    ALL_AGES_LABEL,
)


@pytest.fixture
def completed_episodes_ST_Max_for_new_clients(
    publications: Publications,
) -> pd.DataFrame:
    return publications.ascfr.get_completed_episodes_ST_Max_for_new_clients()


@pytest.fixture
def completed_episodes_ST_Max_for_existing_clients(
    publications: Publications,
) -> pd.Series:
    return publications.ascfr.get_total_completed_episodes_ST_Max_for_existing_clients()


@pytest.fixture
def calculated_measures(
    completed_episodes_ST_Max_for_new_clients: pd.DataFrame,
    completed_episodes_ST_Max_for_existing_clients: pd.DataFrame,
):
    return calculate_measures(
        completed_episodes_ST_Max_for_new_clients,
        completed_episodes_ST_Max_for_existing_clients,
    )


@pytest.fixture
def new_time_series_column(publications):
    return create_new_time_series_column(publications)


def test_create_new_time_series_column(publications: Publications):
    expected_series = pd.Series(
        [
            29850.0,
            216750.0,
            np.nan,
            42920.0,
            47685.0,
            15440.0,
            16460.0,
            12740.0,
            12180.0,
            72040.0,
            0.196,
            0.217,
            0.070,
            0.075,
            0.058,
            0.055,
            0.328,
        ],
        index=params.SHORT_TERM_CARE_TABLE.get_row_order(),
        name=params.PUBLICATION_YEAR,
    )

    actual_series = create_new_time_series_column(publications)

    pd.testing.assert_series_equal(expected_series, actual_series)


def test_create_what_happened_next_series():
    expected_series = pd.Series(
        [np.nan],
        index=[params.SHORT_TERM_CARE_TABLE.ROW_NAMES.WHAT_HAPPENED_NEXT],
        name=params.PUBLICATION_YEAR,
    )

    actual_series = create_what_happened_next_series()

    pd.testing.assert_series_equal(expected_series, actual_series)


def test_calculate_measures(
    completed_episodes_ST_Max_for_new_clients: pd.DataFrame,
    completed_episodes_ST_Max_for_existing_clients: pd.DataFrame,
):
    expected_series = pd.Series(
        {
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.TOTAL_COMPLETED_EPISODES_18_64: 29850.0,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.TOTAL_COMPLETED_EPISODES_65_PLUS: 216750.0,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.EARLY_CESSATION_OF_SERVICE: 42920.0,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT: 47685.0,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.ONGOING_LOW_LEVEL_SUPPORT: 15440.0,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.SHORT_TERM_SUPPORT: 16460.0,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.NO_SERVICES_DECLINED: 12740.0,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.NO_SERVICES_UNVERSAL_SIGNPOSTED: 12180.0,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.NO_SERVICES_NO_IDENTIFIED: 72040.0,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = calculate_measures(
        completed_episodes_ST_Max_for_new_clients,
        completed_episodes_ST_Max_for_existing_clients,
    )

    pd.testing.assert_series_equal(expected_series, actual_series)


def test_calculate_total_completed_episodes_of_ST_Max(
    completed_episodes_ST_Max_for_new_clients: pd.DataFrame,
    completed_episodes_ST_Max_for_existing_clients: pd.DataFrame,
):
    expected_series = pd.Series(
        [29850.0, 216750.0],
        index=[
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.TOTAL_COMPLETED_EPISODES_18_64,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.TOTAL_COMPLETED_EPISODES_65_PLUS,
        ],
        name=params.PUBLICATION_YEAR,
    )

    actual_series = calculate_total_completed_episodes_of_ST_Max(
        completed_episodes_ST_Max_for_new_clients,
        completed_episodes_ST_Max_for_existing_clients,
    )

    pd.testing.assert_series_equal(expected_series, actual_series)


def test_create_series_from_sum_of_completed_episodes_columns():
    df_input = pd.DataFrame(
        {"col_1": [5], "col_2": [10], "col_3": [50]}, index=[ALL_AGES_LABEL]
    )

    expected_index = "index"
    expected_series = pd.Series(
        [15], index=[expected_index], name=params.PUBLICATION_YEAR
    )

    actual_series = create_series_from_sum_of_completed_episodes_columns(
        df_input, ["col_1", "col_2"], expected_index
    )

    pd.testing.assert_series_equal(expected_series, actual_series)


def test_calculate_measure_percentages(
    calculated_measures: pd.Series,
    completed_episodes_ST_Max_for_new_clients: pd.DataFrame,
):
    expected_series = pd.Series(
        {
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.PERCENT_EARLY_CESSATION: 0.19556649,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.PERCENT_LONG_TERM_SUPPORT: 0.21727838,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.PERCENT_ONGOING_LOW_LEVEL_SUPPORT: 0.0703529,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.PERCENT_SHORT_TERM_SUPPORT: 0.07500057,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.PERCENT_NO_SERVICES_DECLINED: 0.05805026,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.PERCENT_NO_SERVICES_UNVERSAL_SIGNPOSTED: 0.0554986,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.PERCENT_NO_SERVICES_NO_IDENTIFIED: 0.3282528,
        },
        name=params.PUBLICATION_YEAR,
    )
    total_completed_episodes_ST_Max_for_new_clients = (
        completed_episodes_ST_Max_for_new_clients.loc["All ages", "Total"]
    )
    actual_series = calculate_measure_percentages(
        total_completed_episodes_ST_Max_for_new_clients, calculated_measures
    )

    pd.testing.assert_series_equal(expected_series, actual_series)
