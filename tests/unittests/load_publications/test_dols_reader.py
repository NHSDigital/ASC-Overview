import pytest
from asc_overview.load_publications.dols_reader.dols_reader import DolsReader
from asc_overview.load_publications.load_publications import load_dols_data


@pytest.fixture
def dols_reader() -> DolsReader:
    return DolsReader(load_dols_data())


def test_get_applications_received(dols_reader: DolsReader):
    expected_applications_received = 256610

    actual_applications_received = dols_reader.get_applications_received()

    assert expected_applications_received == actual_applications_received
