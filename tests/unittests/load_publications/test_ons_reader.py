import pandas as pd
from asc_overview.load_publications.ons_reader import OnsReader
from pytest_mock import MockFixture
import sqlite3
import pytest


@pytest.fixture
def mock_database_connection():
    sqlite3.connect(":memory:")
    connection = sqlite3.connect(":memory:")
    setup_mock_database(connection)
    return connection


def setup_mock_database(connection: sqlite3.Connection):
    pd.DataFrame(
        {
            "POPULATION_COUNT": [33992830, 1, 10464019],
            "YEAR_OF_COUNT": ["2020", "2020", "2020"],
            "GEOGRAPHIC_GROUP_CODE": ["E12", "E12", "E12"],
            "AGE_LOWER": [18, 55, 90],
        },
        index=[0, 1, 2],
    ).to_sql("ONS_POPULATION_V2", connection)


def test_get_population_data_18_64(
    mock_database_connection: sqlite3.Connection, mocker: MockFixture
):
    mocker.patch(
        "asc_overview.load_publications.ons_reader.OnsReader.setup_database_connection",
        return_value=mock_database_connection,
    )

    expected_population = 33992831
    actual_population = OnsReader().get_population_data_18_64()

    assert expected_population == actual_population


def test_get_population_data_65_plus(
    mock_database_connection: sqlite3.Connection, mocker: MockFixture
):
    mocker.patch(
        "asc_overview.load_publications.ons_reader.OnsReader.setup_database_connection",
        return_value=mock_database_connection,
    )

    expected_population = 10464019

    actual_population = OnsReader().get_population_data_65_plus()

    assert expected_population == actual_population
