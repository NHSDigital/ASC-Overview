import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.publications import Publications
from asc_overview.time_series_tables.outcomes_table.outcomes_table import (
    calculate_percent_safeguarding_outcomes,
    create_new_time_series_column,
    get_quality_of_life_section,
    get_safeguarding_outcomes_section,
    get_delayed_transfers_section,
)
from asc_overview.time_series_tables.outcomes_table.outcomes_table_config import (
    OutcomesRowNames,
)


@pytest.fixture
def row_names() -> OutcomesRowNames:
    return params.OUTCOMES_TABLE.ROW_NAMES


def test_create_new_time_series_column(
    publications: Publications, row_names: OutcomesRowNames
):
    expected_series = pd.Series(
        {
            row_names.SERVICE_USER_QUALITY_OF_LIFE_18_64: 19.2,
            row_names.SERVICE_USER_QUALITY_OF_LIFE_65_AND_OVER: 18.8,
            row_names.CARER_QUALITY_OF_LIFE_18_64: "N/A",
            row_names.CARER_QUALITY_OF_LIFE_65_AND_OVER: "N/A",
            row_names.DELAYED_TRANSFERS: "N/A",
            row_names.DELAYED_TRANSFERS_AND_ATTRIBUTABLE: "N/A",
            row_names.FULLY_ACHIEVED: 47915,
            row_names.PARTLY_ACHIEVED: 18770,
            row_names.NOT_ACHIEVED: 3690,
            row_names.PERCENT_FULLY_ACHIEVED: 0.681,
            row_names.PERCENT_PARTLY_ACHIEVED: 0.267,
            row_names.PERCENT_FULLY_OR_PARTLY_ACHIEVED: 0.948,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = create_new_time_series_column(publications)

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_quality_of_life_section(
    publications: Publications, row_names: OutcomesRowNames
):
    expected_series = pd.Series(
        {
            row_names.SERVICE_USER_QUALITY_OF_LIFE_18_64: 19.2,
            row_names.SERVICE_USER_QUALITY_OF_LIFE_65_AND_OVER: 18.8,
            row_names.CARER_QUALITY_OF_LIFE_18_64: "N/A",
            row_names.CARER_QUALITY_OF_LIFE_65_AND_OVER: "N/A",
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = get_quality_of_life_section(publications.ascof)

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_delayed_transfers_section(row_names: OutcomesRowNames):
    expected_series = pd.Series(
        {
            row_names.DELAYED_TRANSFERS: "N/A",
            row_names.DELAYED_TRANSFERS_AND_ATTRIBUTABLE: "N/A",
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = get_delayed_transfers_section()

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_safeguarding_outcomes_section(
    publications: Publications, row_names: OutcomesRowNames
):
    expected_series = pd.Series(
        {
            row_names.FULLY_ACHIEVED: 47915,
            row_names.PARTLY_ACHIEVED: 18770,
            row_names.NOT_ACHIEVED: 3690,
            row_names.PERCENT_FULLY_ACHIEVED: 0.68085258,
            row_names.PERCENT_PARTLY_ACHIEVED: 0.26671403,
            row_names.PERCENT_FULLY_OR_PARTLY_ACHIEVED: 0.94756661,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = get_safeguarding_outcomes_section(publications.safeguarding)

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_calculate_percent_safeguarding_outcomes(row_names: OutcomesRowNames):
    input_series = pd.Series(
        {
            "Fully Achieved": 25,
            "Partially Achieved": 15,
            "Not Achived": 60,
        },
        name=params.PUBLICATION_YEAR,
    )

    expected_series = pd.Series(
        {
            row_names.PERCENT_FULLY_ACHIEVED: 0.25,
            row_names.PERCENT_PARTLY_ACHIEVED: 0.15,
            row_names.PERCENT_FULLY_OR_PARTLY_ACHIEVED: 0.40,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = calculate_percent_safeguarding_outcomes(input_series)

    pd_testing.assert_series_equal(actual_series, expected_series)
