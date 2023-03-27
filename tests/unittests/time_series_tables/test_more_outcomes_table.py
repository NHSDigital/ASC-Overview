import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.publications import Publications
from asc_overview.time_series_tables.more_outcomes_table.more_outcomes_table_config import (
    MoreOutcomesRowNames,
)
from asc_overview.time_series_tables.more_outcomes_table.more_outcomes_table import (
    create_new_time_series_column,
    get_safety_section,
    get_social_contact_section,
)


@pytest.fixture
def row_names() -> MoreOutcomesRowNames:
    return params.MORE_OUTCOMES_TABLE.ROW_NAMES


def test_create_new_time_series_columm(
    publications: Publications, row_names: MoreOutcomesRowNames
):
    expected_series = pd.Series(
        {
            row_names.SERVICE_USER_SAFETY_18_64: 0.709,
            row_names.SERVICE_USER_SAFETY_65_AND_OVER: 0.756,
            row_names.SERVICE_USER_SOCIAL_CONTACT_18_64: 0.368,
            row_names.SERVICE_USER_SOCIAL_CONTACT_65_AND_OVER: 0.327,
            row_names.CARERS_SOCIAL_CONTACT_18_64: "N/A",
            row_names.CARERS_SOCIAL_CONTACT_65_AND_OVER: "N/A",
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = create_new_time_series_column(publications)

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_safety_section(
    publications: Publications, row_names: MoreOutcomesRowNames
):
    expected_series = pd.Series(
        {
            row_names.SERVICE_USER_SAFETY_18_64: 0.709,
            row_names.SERVICE_USER_SAFETY_65_AND_OVER: 0.756,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = get_safety_section(publications.ascof)

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_social_contact_section(
    publications: Publications, row_names: MoreOutcomesRowNames
):
    expected_series = pd.Series(
        {
            row_names.SERVICE_USER_SOCIAL_CONTACT_18_64: 0.368,
            row_names.SERVICE_USER_SOCIAL_CONTACT_65_AND_OVER: 0.327,
            row_names.CARERS_SOCIAL_CONTACT_18_64: "N/A",
            row_names.CARERS_SOCIAL_CONTACT_65_AND_OVER: "N/A",
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = get_social_contact_section(publications.ascof)

    pd_testing.assert_series_equal(actual_series, expected_series)
