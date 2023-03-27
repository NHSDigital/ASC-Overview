import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.load_publications import load_overview_workbook
from asc_overview.load_publications.overview_reader.overview_reader import (
    OverviewReader,
    ALL_YEARS,
)
from asc_overview.time_series_tables.la_expenditure_table.la_expenditure_table_config import (
    LaExpenditureRowNames,
)


@pytest.fixture
def overview_reader() -> OverviewReader:
    return OverviewReader(load_overview_workbook())


@pytest.fixture
def la_expenditure_row_names() -> LaExpenditureRowNames:
    return params.LA_EXPENDITURE_TABLE.ROW_NAMES


def test_get_gross_current_expenditure(
    overview_reader: OverviewReader, la_expenditure_row_names: LaExpenditureRowNames
):
    expected_series = pd.Series(
        {
            "2005-06": 20.17,
            "2006-07": 20.33,
            "2007-08": 20.28,
            "2008-09": 20.73,
            "2009-10": 21.34,
            "2010-11": 21.28,
            "2011-12": 21.19,
            "2012-13": 20.69,
            "2013-14": 20.33,
            "2014-15": 19.86,
            "2015-16": 19.65,
            "2016-17": 19.85,
            "2017-18": 19.96,
            "2018-19": 20.46,
            "2019-20": 20.96,
            "2020-21": 21.24,
        },
        name=la_expenditure_row_names.GROSS_CURRENT_EXPENDITURE,
    )

    actual_series = overview_reader.get_gross_current_expenditure()

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_expenditure_per_citizen(
    overview_reader: OverviewReader, la_expenditure_row_names: LaExpenditureRowNames
):
    expected_series = pd.Series(
        {
            "2005-06": 510.79,
            "2006-07": 510.13,
            "2007-08": 504.09,
            "2008-09": 510.37,
            "2009-10": 520.81,
            "2010-11": 514.38,
            "2011-12": 507.40,
            "2012-13": 491.78,
            "2013-14": 480.00,
            "2014-15": 461.61,
            "2015-16": 455.91,
            "2016-17": 456.59,
            "2017-18": 456.32,
            "2018-19": 464.86,
            "2019-20": 473.62,
            "2020-21": 477.82,
        },
        name=la_expenditure_row_names.GROSS_CURRENT_EXPENDITURE_PER_ADULT,
    )

    actual_series = overview_reader.get_expenditure_per_citizen()

    pd_testing.assert_series_equal(actual_series, expected_series)


def test_get_proportion_la_expenditure(
    overview_reader: OverviewReader, la_expenditure_row_names: LaExpenditureRowNames
):
    df_expected = pd.DataFrame(
        {
            la_expenditure_row_names.PERCENT_LA_OWN_PROVISION: [
                25.0,
                23.2,
                22.2,
                22.1,
                21.9,
                20.6,
            ],
            la_expenditure_row_names.PERCENT_PROVISION_BY_OTHERS: [
                74.0,
                75.8,
                76.9,
                77.1,
                77.4,
                78.5,
            ],
            la_expenditure_row_names.PERCENT_GRANTS_TO_VOLUNTARY_ORGANISATIONS: [
                1.0,
                0.9,
                0.9,
                0.7,
                0.7,
                0.9,
            ],
        },
        index=ALL_YEARS,
    )

    df_actual = overview_reader.get_proportion_la_expenditure()

    pd_testing.assert_frame_equal(df_actual, df_expected)
