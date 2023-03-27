import pandas as pd
from openpyxl import Workbook
from asc_overview.load_publications.publications import Publications
from asc_overview.utilities.output_to_excel import (
    get_worksheet_from_workbook,
)
from asc_overview.utilities.output_to_excel import write_dataframe_to_excel
from asc_overview import params


def add_outcomes_by_la_to_workbook(
    template_workbook: Workbook, publications: Publications
):
    outcomes_by_la_sheet = get_worksheet_from_workbook(
        template_workbook, params.OUTCOMES_BY_LA_TABLE.OVERVIEW_SHEET_NAME
    )

    df_social_contact_by_la = (
        publications.ascof.get_service_user_socal_contact_by_la().sort_index()
    )

    df_feel_safe_by_la = (
        publications.ascof.get_service_user_feel_safe_by_la().sort_index()
    )

    write_dataframe_to_excel(
        outcomes_by_la_sheet,
        df_social_contact_by_la,
        params.OUTCOMES_BY_LA_TABLE.CELL_TO_WRITE_TO_SOCIAL_CONTACT,
    )
    write_dataframe_to_excel(
        outcomes_by_la_sheet,
        df_feel_safe_by_la,
        params.OUTCOMES_BY_LA_TABLE.CELL_TO_WRITE_TO_FEEL_SAFE,
    )
