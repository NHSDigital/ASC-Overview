import pandas as pd
from asc_overview import params
from openpyxl import Workbook
from asc_overview.load_publications.publications import Publications
from asc_overview.load_publications.ascof_reader.ascof_reader import AscofReader
from asc_overview.utilities.reindex_rows import (
    reindex_rows,
)
from asc_overview.load_publications.safeguarding_reader.safeguarding_reader import (
    SafeguardingReader,
)
from asc_overview.utilities.output_to_excel import (
    output_time_series_column_to_workbook,
    get_worksheet_from_workbook,
)


def add_new_outcomes_time_series_column_to_workbook(
    template_workbook: Workbook, publications: Publications
) -> None:
    outcomes_sheet = get_worksheet_from_workbook(
        template_workbook, params.OUTCOMES_TABLE.OVERVIEW_SHEET_NAME
    )

    new_time_series_column = create_new_time_series_column(publications)

    output_time_series_column_to_workbook(
        outcomes_sheet, new_time_series_column, params.OUTCOMES_TABLE.CELL_TO_WRITE_TO
    )


def create_new_time_series_column(publications: Publications) -> pd.Series:
    quality_of_life_section = get_quality_of_life_section(publications.ascof)
    delayed_transfers_section = get_delayed_transfers_section()
    safeguarding_outcomes_section = get_safeguarding_outcomes_section(
        publications.safeguarding
    ).round(3)

    return pd.concat(
        [
            quality_of_life_section,
            delayed_transfers_section,
            safeguarding_outcomes_section,
        ]
    ).pipe(reindex_rows, params.OUTCOMES_TABLE.get_row_order())


def get_quality_of_life_section(ascof_reader: AscofReader):
    service_user_quality_of_life_by_age = (
        ascof_reader.get_service_user_quality_of_life_score_by_age()
    )
    carer_quality_of_life_by_age = ascof_reader.get_carer_quality_of_life_score_by_age()

    return pd.Series(
        [*service_user_quality_of_life_by_age, *carer_quality_of_life_by_age],
        index=[
            params.OUTCOMES_TABLE.ROW_NAMES.SERVICE_USER_QUALITY_OF_LIFE_18_64,
            params.OUTCOMES_TABLE.ROW_NAMES.SERVICE_USER_QUALITY_OF_LIFE_65_AND_OVER,
            params.OUTCOMES_TABLE.ROW_NAMES.CARER_QUALITY_OF_LIFE_18_64,
            params.OUTCOMES_TABLE.ROW_NAMES.CARER_QUALITY_OF_LIFE_65_AND_OVER,
        ],
        name=params.PUBLICATION_YEAR,
    )


def get_delayed_transfers_section():
    """
    The delayed transfers data has been paused indefinitely.
    This means the values for those rows are N/A
    """
    return pd.Series(
        {
            params.OUTCOMES_TABLE.ROW_NAMES.DELAYED_TRANSFERS: "N/A",
            params.OUTCOMES_TABLE.ROW_NAMES.DELAYED_TRANSFERS_AND_ATTRIBUTABLE: "N/A",
        },
        name=params.PUBLICATION_YEAR,
    )


def get_safeguarding_outcomes_section(safeguarding_reader: SafeguardingReader):
    ROW_NAMES = params.OUTCOMES_TABLE.ROW_NAMES
    outcomes = safeguarding_reader.get_safeguarding_outcomes()
    percent_outcomes = calculate_percent_safeguarding_outcomes(outcomes)

    return pd.Series(
        [*outcomes, *percent_outcomes],
        index=[
            ROW_NAMES.FULLY_ACHIEVED,
            ROW_NAMES.PARTLY_ACHIEVED,
            ROW_NAMES.NOT_ACHIEVED,
            ROW_NAMES.PERCENT_FULLY_ACHIEVED,
            ROW_NAMES.PERCENT_PARTLY_ACHIEVED,
            ROW_NAMES.PERCENT_FULLY_OR_PARTLY_ACHIEVED,
        ],
        name=params.PUBLICATION_YEAR,
    )


def calculate_percent_safeguarding_outcomes(safeguarding_outcomes: pd.Series):
    ROW_NAMES = params.OUTCOMES_TABLE.ROW_NAMES

    total_safeguarding_outcomes = safeguarding_outcomes.sum()
    percent_fully_achieved = (
        safeguarding_outcomes.loc["Fully Achieved"] / total_safeguarding_outcomes
    )
    percent_partly_achieved = (
        safeguarding_outcomes.loc["Partially Achieved"] / total_safeguarding_outcomes
    )

    percent_fully_or_partly_achieved = percent_fully_achieved + percent_partly_achieved

    return pd.Series(
        [
            percent_fully_achieved,
            percent_partly_achieved,
            percent_fully_or_partly_achieved,
        ],
        index=[
            ROW_NAMES.PERCENT_FULLY_ACHIEVED,
            ROW_NAMES.PERCENT_PARTLY_ACHIEVED,
            ROW_NAMES.PERCENT_FULLY_OR_PARTLY_ACHIEVED,
        ],
        name=params.PUBLICATION_YEAR,
    )
