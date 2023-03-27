import pytest
import pandas as pd
import pandas.testing as pd_testing
from asc_overview import params
from asc_overview.load_publications.load_publications import load_overview_workbook
from asc_overview.load_publications.overview_reader.overview_reader import (
    OverviewReader,
    ALL_YEARS,
)
from asc_overview.time_series_tables.long_term_care_table.long_term_care_table_config import (
    LongTermCareRowNames,
)


@pytest.fixture
def overview_reader() -> OverviewReader:
    return OverviewReader(load_overview_workbook())


@pytest.fixture
def long_term_care_row_names() -> LongTermCareRowNames:
    return params.LONG_TERM_CARE_TABLE.ROW_NAMES


def test_get_long_term_support_per_population(
    overview_reader: OverviewReader, long_term_care_row_names: LongTermCareRowNames
):
    df_expected = pd.DataFrame(
        {
            long_term_care_row_names.LONG_TERM_SUPPORT_PERCENT_18_64: [
                0.9,
                0.9,
                0.9,
                0.9,
                0.9,
                0.9,
            ],
            long_term_care_row_names.LONG_TERM_SUPPORT_PERCENT_65_PLUS: [
                6.0,
                5.8,
                5.6,
                5.4,
                5.3,
                5.3,
            ],
        },
        index=ALL_YEARS,
    )

    df_actual = overview_reader.get_long_term_support_per_population()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_long_term_support_setting(
    overview_reader: OverviewReader, long_term_care_row_names: LongTermCareRowNames
):
    df_expected = pd.DataFrame(
        {
            long_term_care_row_names.NURSING_OR_RESIDENTIAL_18_64: [
                47450,
                46665,
                46310,
                46015,
                45560,
                44175,
            ],
            long_term_care_row_names.COMMUNITY_18_64: [
                237570,
                244170,
                246080,
                247400,
                244515,
                245515,
            ],
            long_term_care_row_names.NURSING_OR_RESIDENTIAL_65_PLUS: [
                228185,
                224685,
                221390,
                215650,
                218485,
                209860,
            ],
            long_term_care_row_names.COMMUNITY_65_PLUS: [
                359305,
                352915,
                343995,
                332790,
                329965,
                341695,
            ],
        },
        index=ALL_YEARS,
    )

    df_actual = overview_reader.get_long_term_support_setting()

    pd_testing.assert_frame_equal(df_actual, df_expected)


def test_get_primary_support_reason(
    overview_reader: OverviewReader, long_term_care_row_names: LongTermCareRowNames
):
    df_expected = pd.DataFrame(
        {
            long_term_care_row_names.PHYSICAL_SUPPORT_AS_PRIMARY_18_64: [
                86865,
                87845,
                87410,
                85555,
                84725,
                85955,
            ],
            long_term_care_row_names.OTHER_SUPPORT_AS_PRIMARY_18_64: [
                198165,
                202990,
                204975,
                207860,
                205350,
                203730,
            ],
            long_term_care_row_names.PHYSICAL_SUPPORT_AS_PRIMARY_65_PLUS: [
                434230,
                425480,
                415870,
                404855,
                402375,
                408570,
            ],
            long_term_care_row_names.OTHER_SUPPORT_AS_PRIMARY_65_PLUS: [
                153250,
                152125,
                149520,
                143580,
                146080,
                142975,
            ],
        },
        index=ALL_YEARS,
    )

    df_actual = overview_reader.get_primary_support_reason()

    pd_testing.assert_frame_equal(df_actual, df_expected)
