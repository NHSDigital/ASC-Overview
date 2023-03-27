import pytest
import pandas as pd
import numpy as np
from asc_overview import params


@pytest.mark.parametrize(
    "sheet_name",
    [
        (params.NEW_REQUESTS_TABLE.OVERVIEW.SHEET_NAME),
        (params.SHORT_TERM_CARE_TABLE.OVERVIEW_SHEET_NAME),
        (params.LONG_TERM_CARE_TABLE.OVERVIEW_SHEET_NAME),
        (params.LA_EXPENDITURE_TABLE.OVERVIEW_SHEET_NAME),
        (params.SOCIAL_CARE_EXPERIENCE_TABLE.OVERVIEW_SHEET_NAME),
        (params.OUTCOMES_TABLE.OVERVIEW_SHEET_NAME),
        (params.MORE_OUTCOMES_TABLE.OVERVIEW_SHEET_NAME),
        (params.OUTCOMES_BY_LA_TABLE.OVERVIEW_SHEET_NAME),
        (params.WORKFORCE_TABLE.OVERVIEW_SHEET_NAME),
    ],
)
def test_excel_outputs(save_to_excel, sheet_name):
    df_actual = pd.read_excel(
        save_to_excel,
        sheet_name,
    )
    df_actual_numeric = df_actual.apply(pd.to_numeric, errors="coerce")

    df_expected = pd.read_excel(
        f"./tests/test_data/{params.ASC_OVERVIEW_EXAMPLE_FILE_NAME}",
        sheet_name,
    )
    df_expected_numeric = df_expected.apply(pd.to_numeric, errors="coerce")

    is_same_by_cell = (
        np.isclose(df_expected_numeric, df_actual_numeric)
        | (df_expected == df_actual)
        | (df_expected.isna() & df_actual.isna())
    )

    assert is_same_by_cell.all().all()
