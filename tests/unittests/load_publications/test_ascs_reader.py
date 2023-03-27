import pandas as pd
import pandas.testing as pd_testing
import pytest
from asc_overview.load_publications.ascs_reader.ascs_reader import AscsReader
from asc_overview.load_publications.load_publications import load_ascs_publication
from asc_overview import params


@pytest.fixture
def ascs_reader() -> AscsReader:
    return AscsReader(load_ascs_publication())


def test_get_service_user_feelings_themselves(ascs_reader: AscsReader):
    SOCIAL_CARE_EXPERIENCE_ROW_NAMES = params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES

    expected_series = pd.Series(
        {
            SOCIAL_CARE_EXPERIENCE_ROW_NAMES.FEEL_BETTER_ABOUT_SELF: 0.650,
            SOCIAL_CARE_EXPERIENCE_ROW_NAMES.DOES_NOT_AFFECT_SELF: 0.260,
            SOCIAL_CARE_EXPERIENCE_ROW_NAMES.SOMETIMES_UNDERMINES_SELF: 0.077,
            SOCIAL_CARE_EXPERIENCE_ROW_NAMES.COMPLETELY_UNDERMINES_SELF: 0.013,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = ascs_reader.get_service_user_feelings_themselves()

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_service_user_feelings_choice(ascs_reader: AscsReader):
    SOCIAL_CARE_EXPERIENCE_ROW_NAMES = params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES

    expected_series = pd.Series(
        {
            SOCIAL_CARE_EXPERIENCE_ROW_NAMES.HAVE_ENOUGH_CHOICE: 0.682,
            SOCIAL_CARE_EXPERIENCE_ROW_NAMES.DONT_HAVE_ENOUGH_CHOICE: 0.246,
            SOCIAL_CARE_EXPERIENCE_ROW_NAMES.DONT_WANT_CHOICE: 0.072,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = ascs_reader.get_service_user_feelings_choice()

    pd_testing.assert_series_equal(actual_series, expected_series)
