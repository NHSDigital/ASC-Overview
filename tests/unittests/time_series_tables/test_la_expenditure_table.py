import pandas as pd
import numpy as np
from asc_overview import params
from asc_overview.load_publications.publications import Publications
from asc_overview.time_series_tables.la_expenditure_table.la_expenditure_table import (
    calculate_gross_current_expenditure_per_adult_in_pounds,
    calculate_total_adult_population,
    calculate_gross_current_expenditure_in_billions,
    create_how_money_is_spent_section,
    get_current_year_gross_expenditure,
    get_proportion_how_money_is_spent,
    convert_number_to_billions_rounded,
    get_how_money_is_spent_in_billions,
    create_new_time_series_column,
    create_real_terms_figures_section,
)


def test_create_new_time_series_column(publications: Publications):
    expected_series = pd.Series(
        [21.24, 44456850, 477.82, np.nan, 5.35, 20.41, 0.23, 0.206, 0.785, 0.009],
        index=params.LA_EXPENDITURE_TABLE.get_row_order(),
        name=params.PUBLICATION_YEAR,
    )

    actual_series = create_new_time_series_column(publications)

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore


def test_create_real_terms_figures_section(publications: Publications):
    expected_series = pd.Series(
        {
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.GROSS_CURRENT_EXPENDITURE: 21.24,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.ADULT_POPULATION: 44456850,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.GROSS_CURRENT_EXPENDITURE_PER_ADULT: 477.82,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = create_real_terms_figures_section(publications)

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore


def test_create_how_money_is_spent_section(publications: Publications):
    expected_series = pd.Series(
        {
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.HOW_MONEY_SPENT: np.nan,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.LA_OWN_PROVISION: 5.35,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.PROVISION_BY_OTHERS: 20.41,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.GRANTS_TO_VOLUNTARY_ORGANISATIONS: 0.23,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.PERCENT_LA_OWN_PROVISION: 0.206,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.PERCENT_PROVISION_BY_OTHERS: 0.785,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.PERCENT_GRANTS_TO_VOLUNTARY_ORGANISATIONS: 0.009,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = create_how_money_is_spent_section(publications.ascfr)

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore


def test_get_current_year_gross_expenditure():
    input_series = pd.Series({params.PUBLICATION_YEAR: 21242497})
    expected_current_year_gross_expenditure = 21242497

    actual_current_year_gross_expenditure = get_current_year_gross_expenditure(
        input_series
    )

    assert (
        expected_current_year_gross_expenditure == actual_current_year_gross_expenditure
    )


def test_calculate_gross_current_expenditure_in_billions():
    input_current_year_gross_expenditure = 12345678

    expected_gross_current_expenditure = 12.35

    actual_gross_current_expenditure = calculate_gross_current_expenditure_in_billions(
        input_current_year_gross_expenditure
    )

    assert expected_gross_current_expenditure == actual_gross_current_expenditure


def test_calculate_total_adult_population(publications: Publications):
    expected_population = 44456850

    actual_population = calculate_total_adult_population(publications.ons)

    assert expected_population == actual_population


def test_calculate_gross_current_expenditure_per_adult_in_pounds():
    input_population = 87654321
    input_current_year_gross_expenditure = 12345678
    expected_gross_current_expenditure_per_adult = 140.85

    actual_gross_current_expenditure_per_adult = (
        calculate_gross_current_expenditure_per_adult_in_pounds(
            input_current_year_gross_expenditure, input_population
        )
    )

    assert (
        expected_gross_current_expenditure_per_adult
        == actual_gross_current_expenditure_per_adult
    )


def test_get_how_money_is_spent_in_billions():
    input_series = pd.Series(
        {
            "own_provision": 5351104,
            "provision_by_others": 20407573,
            "grants_voluntary_organisations": 234136,
            "total": 25992812,
        }
    )

    expected_series = pd.Series(
        {
            "own_provision": 5.35,
            "provision_by_others": 20.41,
            "grants_voluntary_organisations": 0.23,
            "total": 25.99,
        }
    )

    actual_series = get_how_money_is_spent_in_billions(input_series)

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore


def test_get_proportion_how_money_is_spent():
    input_series = pd.Series(
        {
            "own_provision": 5351104,
            "provision_by_others": 20407573,
            "grants_voluntary_organisations": 234136,
            "total": 25992812,
        }
    )

    expected_series = pd.Series(
        {
            "own_provision": 0.206,
            "provision_by_others": 0.785,
            "grants_voluntary_organisations": 0.009,
            "total": 1,
        }
    )

    actual_series = get_proportion_how_money_is_spent(input_series)

    pd.testing.assert_series_equal(expected_series, actual_series)  # type: ignore


def test_convert_number_to_billions_rounded():
    input_number = 12345678

    expected_converted_number = 12.35

    actual_converted_number = convert_number_to_billions_rounded(input_number)

    assert expected_converted_number == actual_converted_number
