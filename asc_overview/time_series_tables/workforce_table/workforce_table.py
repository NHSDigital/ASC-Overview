import pandas as pd
from openpyxl import Workbook
from asc_overview.load_publications.publications import Publications
from asc_overview.utilities.create_na_series import create_na_series_for_empty_row
from asc_overview.load_publications.workforce_reader.workforce_reader import (
    WorkforceReader,
)
from asc_overview.utilities.reindex_rows import (
    reindex_rows,
)
from asc_overview.utilities.output_to_excel import (
    output_time_series_column_to_workbook,
    get_worksheet_from_workbook,
)
from asc_overview import params


def add_new_workforce_time_series_column_to_workbook(
    template_workbook: Workbook, publications: Publications
) -> None:
    workforce_sheet = get_worksheet_from_workbook(
        template_workbook, params.WORKFORCE_TABLE.OVERVIEW_SHEET_NAME
    )

    new_time_series_column = create_new_time_series_column(publications)

    output_time_series_column_to_workbook(
        workforce_sheet,
        new_time_series_column,
        params.WORKFORCE_TABLE.CELL_TO_WRITE_TO,
        params.WORKFORCE_YEAR,
    )


def create_new_time_series_column(publications: Publications) -> pd.Series:
    all_job_roles = publications.workforce.get_all_job_roles()

    jobs_and_vacancies_section = get_jobs_and_vacancies_section(all_job_roles)
    starters_and_leavers_section = get_starters_and_leavers_section(
        publications.workforce
    )
    type_of_role_empty_series = create_na_series_for_empty_row(
        params.WORKFORCE_TABLE.ROW_NAMES.TYPE_OF_ROLE
    )
    job_roles_section = get_job_roles_section(all_job_roles)
    percent_job_roles_section = get_percent_job_roles_section(job_roles_section)

    return (
        pd.concat(
            [
                jobs_and_vacancies_section,
                starters_and_leavers_section,
                type_of_role_empty_series,
                job_roles_section,
                percent_job_roles_section,
            ]
        )
        .pipe(reindex_rows, params.WORKFORCE_TABLE.get_row_order())
        .round(3)
    )


def get_jobs_and_vacancies_section(all_job_roles: pd.Series) -> pd.Series:
    jobs_and_vacancies = all_job_roles.loc["All job roles"]

    jobs_and_vacancies = jobs_and_vacancies.set_axis(
        [
            params.WORKFORCE_TABLE.ROW_NAMES.JOBS,
            params.WORKFORCE_TABLE.ROW_NAMES.VACANCIES,
        ]
    )

    return jobs_and_vacancies


def get_starters_and_leavers_section(workforce_reader: WorkforceReader) -> pd.Series:
    return pd.Series(
        {
            params.WORKFORCE_TABLE.ROW_NAMES.NEW_STARTERS: workforce_reader.get_new_starters(),
            params.WORKFORCE_TABLE.ROW_NAMES.LEAVERS: workforce_reader.get_leavers(),
        },
        name=params.PUBLICATION_YEAR,
    )


def get_job_roles_section(all_job_roles: pd.Series) -> pd.Series:
    REQUIRED_JOB_ROLES = [
        "Direct care",
        "Manager / Supervisor",
        "Professional",
        "Other",
    ]
    REQUIRED_JOB_ROLE_BREAKDOWN = "Employees"
    job_roles = all_job_roles.loc[REQUIRED_JOB_ROLES, REQUIRED_JOB_ROLE_BREAKDOWN]  # type: ignore

    return job_roles.set_axis(
        [
            params.WORKFORCE_TABLE.ROW_NAMES.DIRECT_CARE,
            params.WORKFORCE_TABLE.ROW_NAMES.MANAGER_SUPERVISOR,
            params.WORKFORCE_TABLE.ROW_NAMES.PROFESSIONAL,
            params.WORKFORCE_TABLE.ROW_NAMES.OTHER,
        ]
    )


def get_percent_job_roles_section(job_roles_section: pd.Series) -> pd.Series:
    percent_job_roles = job_roles_section / job_roles_section.sum()

    return percent_job_roles.set_axis(
        [
            params.WORKFORCE_TABLE.ROW_NAMES.PERCENT_DIRECT_CARE,
            params.WORKFORCE_TABLE.ROW_NAMES.PERCENT_MANAGER_SUPERVISOR,
            params.WORKFORCE_TABLE.ROW_NAMES.PERCENT_PROFESSIONAL,
            params.WORKFORCE_TABLE.ROW_NAMES.PERCENT_OTHER,
        ]
    )
