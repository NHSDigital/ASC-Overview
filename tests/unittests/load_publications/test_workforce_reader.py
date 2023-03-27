import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview.load_publications.workforce_reader.workforce_reader import (
    WorkforceReader,
)
from asc_overview.load_publications.workforce_reader.workforce_loading_config import (
    JOB_ROLES,
    JOB_ROLE_BREAKDOWNS,
)
from asc_overview.load_publications.load_publications import load_workforce_publication
from asc_overview import params


@pytest.fixture(scope="module")
def workforce_reader():
    return WorkforceReader(load_workforce_publication())


def test_get_all_job_roles(workforce_reader: WorkforceReader):
    expected_series = pd.Series(
        [
            105780,
            8035,
            46945,
            3305,
            17470,
            1030,
            19320,
            1995,
            22045,
            1700,
        ],
        index=pd.MultiIndex.from_product(
            [
                JOB_ROLES,
                JOB_ROLE_BREAKDOWNS,
            ]
        ),
        name=params.PUBLICATION_YEAR,
    )

    actual_series = workforce_reader.get_all_job_roles()

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_new_starters(workforce_reader: WorkforceReader):
    expected_new_starters = 14385

    actual_new_starters = workforce_reader.get_new_starters()

    assert actual_new_starters == expected_new_starters


def test_get_leavers(workforce_reader: WorkforceReader):
    expected_leavers = 13320

    actual_leavers = workforce_reader.get_leavers()

    assert actual_leavers == expected_leavers
