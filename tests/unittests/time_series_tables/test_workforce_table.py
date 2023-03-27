import pytest
import numpy as np
import pandas as pd
import pandas.testing as pd_testing
from asc_overview.load_publications.publications import Publications
from asc_overview.time_series_tables.workforce_table.workforce_table import (
    create_new_time_series_column,
    get_job_roles_section,
    get_jobs_and_vacancies_section,
    get_percent_job_roles_section,
    get_starters_and_leavers_section,
)
from asc_overview import params


@pytest.fixture
def all_job_roles(publications: Publications):
    return publications.workforce.get_all_job_roles()


def test_create_new_time_series_column(publications: Publications):
    ROW_NAMES = params.WORKFORCE_TABLE.ROW_NAMES
    expected_series = pd.Series(
        {
            ROW_NAMES.JOBS: 105780,
            ROW_NAMES.VACANCIES: 8035,
            ROW_NAMES.NEW_STARTERS: 14385,
            ROW_NAMES.LEAVERS: 13320,
            ROW_NAMES.TYPE_OF_ROLE: np.nan,
            ROW_NAMES.DIRECT_CARE: 46945,
            ROW_NAMES.MANAGER_SUPERVISOR: 17470,
            ROW_NAMES.PROFESSIONAL: 19320,
            ROW_NAMES.OTHER: 22045,
            ROW_NAMES.PERCENT_DIRECT_CARE: 0.444,
            ROW_NAMES.PERCENT_MANAGER_SUPERVISOR: 0.165,
            ROW_NAMES.PERCENT_PROFESSIONAL: 0.183,
            ROW_NAMES.PERCENT_OTHER: 0.208,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = create_new_time_series_column(publications)

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_jobs_and_vacancies_section(all_job_roles: pd.Series):
    expected_series = pd.Series(
        {
            params.WORKFORCE_TABLE.ROW_NAMES.JOBS: 105780,
            params.WORKFORCE_TABLE.ROW_NAMES.VACANCIES: 8035,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = get_jobs_and_vacancies_section(all_job_roles)

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_starters_and_leavers_section(publications: Publications):
    expected_series = pd.Series(
        {
            params.WORKFORCE_TABLE.ROW_NAMES.NEW_STARTERS: 14385,
            params.WORKFORCE_TABLE.ROW_NAMES.LEAVERS: 13320,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = get_starters_and_leavers_section(publications.workforce)

    pd_testing.assert_series_equal(expected_series, actual_series)


def test_get_job_roles_section(all_job_roles: pd.Series):
    expected_series = pd.Series(
        {
            params.WORKFORCE_TABLE.ROW_NAMES.DIRECT_CARE: 46945,
            params.WORKFORCE_TABLE.ROW_NAMES.MANAGER_SUPERVISOR: 17470,
            params.WORKFORCE_TABLE.ROW_NAMES.PROFESSIONAL: 19320,
            params.WORKFORCE_TABLE.ROW_NAMES.OTHER: 22045,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = get_job_roles_section(all_job_roles)

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_percent_job_roles_section():
    input_series = pd.Series(
        {
            params.WORKFORCE_TABLE.ROW_NAMES.DIRECT_CARE: 50,
            params.WORKFORCE_TABLE.ROW_NAMES.MANAGER_SUPERVISOR: 25,
            params.WORKFORCE_TABLE.ROW_NAMES.PROFESSIONAL: 15,
            params.WORKFORCE_TABLE.ROW_NAMES.OTHER: 10,
        },
        name=params.PUBLICATION_YEAR,
    )

    expected_series = pd.Series(
        {
            params.WORKFORCE_TABLE.ROW_NAMES.PERCENT_DIRECT_CARE: 0.5,
            params.WORKFORCE_TABLE.ROW_NAMES.PERCENT_MANAGER_SUPERVISOR: 0.25,
            params.WORKFORCE_TABLE.ROW_NAMES.PERCENT_PROFESSIONAL: 0.15,
            params.WORKFORCE_TABLE.ROW_NAMES.PERCENT_OTHER: 0.1,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = get_percent_job_roles_section(input_series)

    pd_testing.assert_series_equal(actual_series, expected_series)
