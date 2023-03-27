import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from asc_overview import params
from asc_overview.utilities.reindex_rows import reindex_rows
from asc_overview.load_publications.ons_reader import OnsReader
from asc_overview.load_publications.publications import Publications
from asc_overview.utilities.output_to_excel import (
    output_time_series_column_to_workbook,
    get_worksheet_from_workbook,
)
from asc_overview.load_publications.acfr_reader.ascfr_reader import AscfrReader


def add_new_la_expenditure_time_series_column_to_workbook(
    template_workbook: Workbook, publications: Publications
) -> None:
    la_expenditure_sheet = get_worksheet_from_workbook(
        template_workbook, params.LA_EXPENDITURE_TABLE.OVERVIEW_SHEET_NAME
    )

    new_time_series_column = create_new_time_series_column(publications)

    output_time_series_column_to_workbook(
        la_expenditure_sheet,
        new_time_series_column,
        params.LA_EXPENDITURE_TABLE.CELL_TO_WRITE_TO,
    )


def create_new_time_series_column(publications: Publications):
    real_term_figures_section = create_real_terms_figures_section(publications)
    how_money_is_spent_section = create_how_money_is_spent_section(publications.ascfr)

    return pd.concat([real_term_figures_section, how_money_is_spent_section]).pipe(
        reindex_rows, params.LA_EXPENDITURE_TABLE.get_row_order()
    )


def create_real_terms_figures_section(publications: Publications):
    real_terms_figures_by_year = publications.ascfr.get_real_term_figures_by_year()
    current_year_gross_expenditure = get_current_year_gross_expenditure(
        real_terms_figures_by_year
    )
    total_adult_population = calculate_total_adult_population(publications.ons)
    return pd.Series(
        {
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.GROSS_CURRENT_EXPENDITURE: calculate_gross_current_expenditure_in_billions(
                current_year_gross_expenditure
            ),
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.ADULT_POPULATION: total_adult_population,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.GROSS_CURRENT_EXPENDITURE_PER_ADULT: calculate_gross_current_expenditure_per_adult_in_pounds(
                current_year_gross_expenditure, total_adult_population
            ),
        },
        name=params.PUBLICATION_YEAR,
    )


def create_how_money_is_spent_section(ascfr_reader: AscfrReader) -> pd.Series:
    ROW_NAMES = params.LA_EXPENDITURE_TABLE.ROW_NAMES
    how_money_is_spent_figures_by_measure = (
        ascfr_reader.get_how_money_spent_figures_by_measure()
    )

    how_money_is_spent_in_billions = get_how_money_is_spent_in_billions(
        how_money_is_spent_figures_by_measure
    ).rename(
        {
            "own_provision": ROW_NAMES.LA_OWN_PROVISION,
            "provision_by_others": ROW_NAMES.PROVISION_BY_OTHERS,
            "grants_voluntary_organisations": ROW_NAMES.GRANTS_TO_VOLUNTARY_ORGANISATIONS,
        }
    )
    percent_how_money_is_spent = get_proportion_how_money_is_spent(
        how_money_is_spent_figures_by_measure
    ).rename(
        {
            "own_provision": ROW_NAMES.PERCENT_LA_OWN_PROVISION,
            "provision_by_others": ROW_NAMES.PERCENT_PROVISION_BY_OTHERS,
            "grants_voluntary_organisations": ROW_NAMES.PERCENT_GRANTS_TO_VOLUNTARY_ORGANISATIONS,
        }
    )

    return pd.concat(
        [
            create_how_money_is_spent_series(),
            how_money_is_spent_in_billions,
            percent_how_money_is_spent,
        ]
    ).drop(["total"])


def create_how_money_is_spent_series():
    return pd.Series(
        {params.LA_EXPENDITURE_TABLE.ROW_NAMES.HOW_MONEY_SPENT: np.nan},
        name=params.PUBLICATION_YEAR,
    )


def get_current_year_gross_expenditure(real_term_figures_by_year: pd.Series) -> int:
    return real_term_figures_by_year.loc[params.PUBLICATION_YEAR]


def calculate_gross_current_expenditure_in_billions(
    current_year_gross_expenditure: int,
) -> float:
    return convert_number_to_billions_rounded(current_year_gross_expenditure)


def calculate_total_adult_population(ons_reader: OnsReader) -> int:
    return (
        ons_reader.get_population_data_18_64()
        + ons_reader.get_population_data_65_plus()
    )


def calculate_gross_current_expenditure_per_adult_in_pounds(
    input_current_year_gross_expenditure: int, total_adult_population: int
) -> float:
    return round(
        (input_current_year_gross_expenditure * 1000) / total_adult_population, 2
    )


def get_how_money_is_spent_in_billions(
    how_money_is_spent_figures_by_measure: pd.Series,
) -> pd.Series:
    return how_money_is_spent_figures_by_measure.apply(  # type: ignore
        convert_number_to_billions_rounded
    )


def get_proportion_how_money_is_spent(
    how_money_is_spent_figures_by_measure: pd.Series,
) -> pd.Series:
    return (
        (
            how_money_is_spent_figures_by_measure
            / how_money_is_spent_figures_by_measure.loc["total"]
        )
    ).round(3)


def convert_number_to_billions_rounded(number_to_convert: int) -> float:
    return round(number_to_convert / 1000000, 2)
