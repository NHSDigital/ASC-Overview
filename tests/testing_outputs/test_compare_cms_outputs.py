import pytest
import pandas as pd
import numpy as np
from asc_overview.cms_tables import cms_filenames as name


@pytest.mark.parametrize(
    "excel_filename",
    [
        name.NEW_REQUESTS_FOR_SUPPORT,
        name.CHANGE_IN_NEW_REQUESTS,
        name.NEW_REQUESTS_PER_POPULATION,
        name.DOLS_REQUESTS,
        name.SAEFEGUARDING_REQUESTS,
        name.CHANGE_IN_SAFEGUARDING_AND_DOLS,
        name.SHORT_TERM_SUPPORT,
        name.WHAT_HAPPENED_NEXT,
        name.LONG_TERM_SUPPORT,
        name.LONG_TERM_SUPPORT_SETTING,
        name.PRIMARY_SUPPORT_REASON,
        name.GROSS_CURRENT_EXPENDITURE,
        name.GROSS_CURRENT_EXPENDITURE_PER_CITIZEN,
        name.LA_EXPENDITURE,
        name.JOBS,
        name.VACANCIES,
        name.STARTERS_AND_LEAVERS,
        name.TYPE_OF_ROLE,
        name.SERVICE_USER_SATISFACTION,
        name.SERVICE_USER_THEMSELVES,
        name.SERVICE_USER_CHOICE,
        name.CARER_SATISFACTION,
        name.SERVICE_USER_QUALITY_OF_LIFE,
        name.CARER_QUALITY_OF_LIFE,
        name.SAFEGUARDING_ENQUIRIES,
        name.SERVICE_USER_SAFETY,
        name.SERVICE_USER_SOCIAL_CONTACT,
        name.CARER_SOCIAL_CONTACT,
    ],
)
def test_excel_outputs(save_cms_to_excel: str, excel_filename: str):
    df_actual = pd.read_excel(f"{save_cms_to_excel}/{excel_filename}", "Sheet")
    df_actual_numeric = df_actual.apply(pd.to_numeric, errors="coerce")

    df_expected = pd.read_excel(
        f"./tests/test_data/cms_tables/{excel_filename}", "Sheet1"
    )
    df_expected_numeric = df_expected.apply(pd.to_numeric, errors="coerce")

    is_same_by_cell = (
        np.isclose(df_expected_numeric, df_actual_numeric)
        | (df_expected == df_actual)
        | (df_expected.isna() & df_actual.isna())
    )

    assert is_same_by_cell.all().all()
