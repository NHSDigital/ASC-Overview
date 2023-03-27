from openpyxl import Workbook
import pandas as pd
import numpy as np
from asc_overview import params
from asc_overview.load_publications.publications import Publications
from asc_overview.utilities.output_to_excel import (
    output_time_series_column_to_workbook,
    get_worksheet_from_workbook,
)
from asc_overview.utilities.reindex_rows import (
    reindex_rows,
)

ALL_AGES_LABEL = "All ages"


def add_new_short_term_care_time_series_column_to_workbook(
    template_workbook: Workbook, publications: Publications
):
    short_term_care_sheet = get_worksheet_from_workbook(
        template_workbook, params.SHORT_TERM_CARE_TABLE.OVERVIEW_SHEET_NAME
    )

    new_time_series_column = create_new_time_series_column(publications)

    output_time_series_column_to_workbook(
        short_term_care_sheet,
        new_time_series_column,
        params.SHORT_TERM_CARE_TABLE.CELL_TO_WRITE_TO,
    )


def create_new_time_series_column(publications: Publications) -> pd.Series:
    completed_episodes_ST_Max_for_new_clients = (
        publications.ascfr.get_completed_episodes_ST_Max_for_new_clients()
    )
    completed_episodes_ST_Max_for_existing_clients = (
        publications.ascfr.get_total_completed_episodes_ST_Max_for_existing_clients()
    )

    total_completed_episodes_ST_Max_for_new_clients = (
        completed_episodes_ST_Max_for_new_clients.loc["All ages", "Total"]
    )

    calculated_measures = calculate_measures(
        completed_episodes_ST_Max_for_new_clients,
        completed_episodes_ST_Max_for_existing_clients,
    )

    calculated_measure_percentages = calculate_measure_percentages(
        total_completed_episodes_ST_Max_for_new_clients,
        calculated_measures,
    )

    what_happened_next_series = create_what_happened_next_series()

    return (
        pd.concat(
            [
                calculated_measures,
                calculated_measure_percentages,
                what_happened_next_series,
            ]
        )
        .pipe(reindex_rows, params.SHORT_TERM_CARE_TABLE.get_row_order())
        .round(3)
    )


def create_what_happened_next_series():
    """
    This function adds in the What happened next for new clients (all ages) row
    for the excel output.
    """
    return pd.Series(
        [np.nan],
        index=[params.SHORT_TERM_CARE_TABLE.ROW_NAMES.WHAT_HAPPENED_NEXT],
        name=params.PUBLICATION_YEAR,
    )


def calculate_measures(
    completed_episodes_ST_Max_for_new_clients: pd.DataFrame,
    completed_episodes_ST_Max_for_existing_clients: pd.DataFrame,
) -> pd.Series:
    total_completed_episodes_of_ST_Max = calculate_total_completed_episodes_of_ST_Max(
        completed_episodes_ST_Max_for_new_clients,
        completed_episodes_ST_Max_for_existing_clients,
    )

    ROW_NAMES = params.SHORT_TERM_CARE_TABLE.ROW_NAMES
    COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES = (
        params.SHORT_TERM_CARE_TABLE.COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES
    )

    COLUMNS_TO_SUM_BY_MEASURE_NAME = {
        ROW_NAMES.EARLY_CESSATION_OF_SERVICE: [
            COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES.EARLY_CESSATION_OF_SERVICE_COLUMN_NAME,
            COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES.EARLY_CESSATION_OF_SERVICE_NHS_FUNDED_COLUMN_NAME,
        ],
        ROW_NAMES.LONG_TERM_SUPPORT: [
            COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES.EARLY_CESSATION_OF_SERVICE_LONG_TERM_SUPPORT,
            COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES.LONG_TERM_SUPPORT,
        ],
        ROW_NAMES.ONGOING_LOW_LEVEL_SUPPORT: [
            COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES.ONGOING_LOW_LEVEL_SUPPORT
        ],
        ROW_NAMES.SHORT_TERM_SUPPORT: [
            COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES.SHORT_TERM_SUPPORT
        ],
        ROW_NAMES.NO_SERVICES_DECLINED: [
            COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES.NO_SERVICES_DECLINED,
            COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES.NO_SERVICES_SELF_FUNDING,
        ],
        ROW_NAMES.NO_SERVICES_UNVERSAL_SIGNPOSTED: [
            COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES.NO_SERVICES_UNVERSAL_SIGNPOSTED
        ],
        ROW_NAMES.NO_SERVICES_NO_IDENTIFIED: [
            COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES.NO_SERVICES_NO_IDENTIFIED
        ],
    }

    measures = [total_completed_episodes_of_ST_Max]
    for measure_name, columns_to_sum in COLUMNS_TO_SUM_BY_MEASURE_NAME.items():
        measure_series = create_series_from_sum_of_completed_episodes_columns(
            completed_episodes_ST_Max_for_new_clients, columns_to_sum, measure_name
        )
        measures.append(measure_series)

    return pd.concat(measures)


def calculate_total_completed_episodes_of_ST_Max(
    completed_episodes_ST_Max_for_new_clients: pd.DataFrame,
    completed_episodes_ST_Max_for_existing_clients: pd.DataFrame,
) -> pd.Series:
    completed_episodes_ST_Max = (
        completed_episodes_ST_Max_for_existing_clients["Total"]
        + completed_episodes_ST_Max_for_new_clients["Total"]
    ).loc[["18-64", "65 and over"]]

    return pd.Series(
        [*completed_episodes_ST_Max],
        index=[
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.TOTAL_COMPLETED_EPISODES_18_64,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.TOTAL_COMPLETED_EPISODES_65_PLUS,
        ],
        name=params.PUBLICATION_YEAR,
    )


def create_series_from_sum_of_completed_episodes_columns(
    completed_episodes_ST_Max_for_new_clients: pd.DataFrame,
    columns_to_sum: list[str],
    index_name_for_series: str,
):
    measure_value = completed_episodes_ST_Max_for_new_clients.loc[
        ALL_AGES_LABEL, columns_to_sum
    ].sum()

    return pd.Series(
        [measure_value], index=[index_name_for_series], name=params.PUBLICATION_YEAR
    )


def calculate_measure_percentages(
    total_completed_episodes_ST_Max_for_new_clients: int, calculated_measures: pd.Series
) -> pd.Series:
    measure_row_names = params.SHORT_TERM_CARE_TABLE.get_measure_names()

    measure_percentages = (
        calculated_measures[measure_row_names]
        / total_completed_episodes_ST_Max_for_new_clients
    )

    measure_percentages = measure_percentages.rename(lambda x: "% " + x)

    return pd.Series(measure_percentages, name=params.PUBLICATION_YEAR)
