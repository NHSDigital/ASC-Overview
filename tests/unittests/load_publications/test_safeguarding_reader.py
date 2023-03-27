import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.safeguarding_reader.safeguarding_reader import (
    SafeguardingReader,
)
from asc_overview.load_publications.load_publications import (
    load_safeguarding_publication,
)


@pytest.fixture
def safeguarding_reader() -> SafeguardingReader:
    return SafeguardingReader(load_safeguarding_publication())


def test_get_concerns_raised(safeguarding_reader: SafeguardingReader):
    expected_concerns_raised = 498260

    actual_concerns_raised = safeguarding_reader.get_concerns_raised()

    assert expected_concerns_raised == actual_concerns_raised


def test_get_safeguarding_outcomes(safeguarding_reader: SafeguardingReader):
    expected_series = pd.Series(
        [47915, 18770, 3690],
        index=["Fully Achieved", "Partially Achieved", "Not Achieved"],
        name=params.PUBLICATION_YEAR,
    )

    actual_series = safeguarding_reader.get_safeguarding_outcomes()

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_concerns_raised_by_region(safeguarding_reader: SafeguardingReader):
    expected_series = pd.Series(
        {
            "North East": 40155,
            "North West": 67140,
            "Yorkshire and The Humber": 46320,
            "East Midlands": 35390,
            "West Midlands": 48310,
            "East of England": 54665,
            "London": 63310,
            "South East": 88210,
            "South West": 54760,
        },
        name=params.PUBLICATION_YEAR,
    )

    actual_series = safeguarding_reader.get_concerns_raised_by_region()

    pd_testing.assert_series_equal(actual_series, expected_series)
