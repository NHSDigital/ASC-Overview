import pandas as pd
import numpy as np
from openpyxl import Workbook
from asc_overview.load_publications.ascof_reader.ascof_reader import AscofReader
from asc_overview.load_publications.publications import Publications
from asc_overview import params
from asc_overview.utilities.output_to_excel import (
    output_time_series_column_to_workbook,
    get_worksheet_from_workbook,
)
from asc_overview.utilities.reindex_rows import (
    reindex_rows,
)
from asc_overview.utilities.create_na_series import create_na_series_for_empty_row


def add_new_social_care_experience_time_series_column_to_workbook(
    template_workbook: Workbook, publications: Publications
):
    social_care_experience_sheet = get_worksheet_from_workbook(
        template_workbook, params.SOCIAL_CARE_EXPERIENCE_TABLE.OVERVIEW_SHEET_NAME
    )

    new_time_series_column = create_new_time_series_column(publications)

    output_time_series_column_to_workbook(
        social_care_experience_sheet,
        new_time_series_column,
        params.SOCIAL_CARE_EXPERIENCE_TABLE.CELL_TO_WRITE_TO,
    )


def create_new_time_series_column(publications: Publications) -> pd.Series:
    service_user_satisfaction_by_age = get_service_user_satisfaction_section(
        publications.ascof
    )

    carer_satisfaction_by_age = get_carer_percentage_satisfaction_section(
        publications.ascof
    )

    service_user_feelings_themselves_empty_series = create_na_series_for_empty_row(
        params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES.SERVICE_USER_FEELINGS
    )

    service_user_feelings_themselves = (
        publications.ascs.get_service_user_feelings_themselves()
    )

    service_user_feelings_choice_empty_series = create_na_series_for_empty_row(
        params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES.SERVICE_USERS_CHOICE
    )
    service_user_feelings_choice = publications.ascs.get_service_user_feelings_choice()
    return pd.concat(
        [
            service_user_satisfaction_by_age,
            carer_satisfaction_by_age,
            service_user_feelings_themselves_empty_series,
            service_user_feelings_themselves,
            service_user_feelings_choice_empty_series,
            service_user_feelings_choice,
        ]
    ).pipe(reindex_rows, params.SOCIAL_CARE_EXPERIENCE_TABLE.get_row_order())


def get_service_user_satisfaction_section(ascof_reader: AscofReader) -> pd.Series:
    return ascof_reader.get_service_user_percentage_satisfaction_by_age().set_axis(
        [
            params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES.SERVICE_USER_SATISFACTION_18_64,
            params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES.SERVICE_USER_SATISFACTION_65_AND_OVER,
        ]
    )


def get_carer_percentage_satisfaction_section(ascof_reader: AscofReader) -> pd.Series:
    return ascof_reader.get_carer_percentage_satisfaction_by_age().set_axis(
        [
            params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES.CARER_SATISFACTION_18_64,
            params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES.CARER_SATISFACTION_65_AND_OVER,
        ]
    )
