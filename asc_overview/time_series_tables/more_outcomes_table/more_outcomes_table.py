import pandas as pd
from openpyxl import Workbook
from asc_overview import params
from asc_overview.load_publications.publications import Publications
from asc_overview.load_publications.ascof_reader.ascof_reader import AscofReader
from asc_overview.utilities.output_to_excel import output_time_series_column_to_workbook
from asc_overview.utilities.output_to_excel import get_worksheet_from_workbook
from asc_overview.utilities.reindex_rows import (
    reindex_rows,
)


def add_new_more_outcomes_time_series_column_to_workbook(
    template_workbook: Workbook, publications: Publications
) -> None:
    more_outcomes_sheet = get_worksheet_from_workbook(
        template_workbook, params.MORE_OUTCOMES_TABLE.OVERVIEW_SHEET_NAME
    )

    new_time_series_column = create_new_time_series_column(publications)

    output_time_series_column_to_workbook(
        more_outcomes_sheet,
        new_time_series_column,
        params.MORE_OUTCOMES_TABLE.CELL_TO_WRITE_TO,
    )


def create_new_time_series_column(publications: Publications) -> pd.Series:
    safety_section = get_safety_section(publications.ascof)
    social_contact_section = get_social_contact_section(publications.ascof)
    return pd.concat([safety_section, social_contact_section]).pipe(
        reindex_rows, params.MORE_OUTCOMES_TABLE.get_row_order()
    )


def get_safety_section(ascof_reader: AscofReader) -> pd.Series:
    safety_section_row_names = [
        params.MORE_OUTCOMES_TABLE.ROW_NAMES.SERVICE_USER_SAFETY_18_64,
        params.MORE_OUTCOMES_TABLE.ROW_NAMES.SERVICE_USER_SAFETY_65_AND_OVER,
    ]

    return ascof_reader.get_service_user_safety().set_axis(safety_section_row_names)


def get_social_contact_section(ascof_reader: AscofReader) -> pd.Series:
    ROW_NAMES = params.MORE_OUTCOMES_TABLE.ROW_NAMES
    social_contact_row_names = [
        ROW_NAMES.SERVICE_USER_SOCIAL_CONTACT_18_64,
        ROW_NAMES.SERVICE_USER_SOCIAL_CONTACT_65_AND_OVER,
        ROW_NAMES.CARERS_SOCIAL_CONTACT_18_64,
        ROW_NAMES.CARERS_SOCIAL_CONTACT_65_AND_OVER,
    ]

    service_user_social_contact = ascof_reader.get_service_user_social_contact_by_age()
    carer_social_contact = ascof_reader.get_carer_social_contact_by_age()

    return pd.concat([service_user_social_contact, carer_social_contact]).set_axis(
        social_contact_row_names
    )
