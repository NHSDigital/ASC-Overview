from typing import NamedTuple
from openpyxl import Workbook
import pandas as pd
from asc_overview import params
from asc_overview.load_publications.publications import Publications
from asc_overview.utilities.calc_year_on_year_proportion_growth import (
    calc_year_on_year_proportion_growth,
)
from asc_overview.utilities.load_from_excel import load_workbook_range_as_dataframe
from asc_overview.utilities.output_to_excel import (
    output_time_series_column_to_workbook,
    get_worksheet_from_workbook,
)
from asc_overview.utilities.reindex_rows import (
    reindex_rows,
)


class NewRequestsForSupport(NamedTuple):
    new_requests_for_support_by_age: pd.Series
    new_requests_for_support_proportion_growth_by_age: pd.Series


def add_new_requests_time_series_column_to_workbook(
    template_workbook: Workbook, publications: Publications
):
    new_requests_sheet = get_worksheet_from_workbook(
        template_workbook, params.NEW_REQUESTS_TABLE.OVERVIEW.SHEET_NAME
    )

    existing_time_series_data = load_workbook_range_as_dataframe(
        params.NEW_REQUESTS_TABLE.OVERVIEW.WORKBOOK_RANGE,
        new_requests_sheet,
    )

    new_time_series_column = create_new_time_series_column(
        existing_time_series_data, publications
    )

    output_time_series_column_to_workbook(
        new_requests_sheet,
        new_time_series_column,
        params.NEW_REQUESTS_TABLE.CELL_TO_WRITE_TO,
    )


def create_new_time_series_column(
    existing_time_series_data: pd.DataFrame, publications: Publications
) -> pd.Series:
    dols_applications_received = calculate_dols_applications_received(
        publications, existing_time_series_data
    )
    safeguarding_concerns_raised = calculate_safeguarding_concerns_raised(
        publications, existing_time_series_data
    )

    new_requests_for_support = calculate_new_requests_for_support_section(
        existing_time_series_data, publications
    )

    return (
        pd.concat(
            [
                dols_applications_received,
                safeguarding_concerns_raised,
                new_requests_for_support.new_requests_for_support_by_age,
                new_requests_for_support.new_requests_for_support_proportion_growth_by_age,
            ]
        )
        .pipe(reindex_rows, params.NEW_REQUESTS_TABLE.get_row_order())
        .round(3)
    )


def calculate_dols_applications_received(
    publications: Publications, existing_time_series_data: pd.DataFrame
) -> pd.Series:
    APPLICATIONS_RECEIVED_NAME = (
        params.NEW_REQUESTS_TABLE.ROW_NAMES.DOLS_APPLICATIONS_RECEIVED_NAME
    )
    YEAR_ON_YEAR_APPLICATIONS_RECEIVED_NAME = (
        params.NEW_REQUESTS_TABLE.ROW_NAMES.DOLS_YEAR_ON_YEAR_APPLICATIONS_RECEIVED_NAME
    )
    dols_applications_received = publications.dols.get_applications_received()

    dols_applications_proportion_growth = calc_year_on_year_proportion_growth(
        dols_applications_received,
        existing_time_series_data.loc[  # type: ignore
            APPLICATIONS_RECEIVED_NAME,
            params.PREVIOUS_PUBLICATION_YEAR,
        ],
    )
    return pd.Series(
        {
            APPLICATIONS_RECEIVED_NAME: dols_applications_received,
            YEAR_ON_YEAR_APPLICATIONS_RECEIVED_NAME: dols_applications_proportion_growth,
        },
        name=params.PUBLICATION_YEAR,
    )


def calculate_safeguarding_concerns_raised(
    publications: Publications, existing_time_series_data: pd.DataFrame
) -> pd.Series:
    CONCERNS_RAISED_NAME = (
        params.NEW_REQUESTS_TABLE.ROW_NAMES.SAFEGUARDING_CONCERNS_RAISED_NAME
    )
    YEAR_ON_YEAR_CONCERNS_RAISED_NAME = (
        params.NEW_REQUESTS_TABLE.ROW_NAMES.SAFEGUARDING_YEAR_ON_YEAR_CONCERNS_RAISED_NAME
    )

    safeguarding_concerns_raised = publications.safeguarding.get_concerns_raised()
    safeguarding_concerns_raised_proportion_growth = (
        calc_year_on_year_proportion_growth(
            safeguarding_concerns_raised,
            existing_time_series_data.loc[
                CONCERNS_RAISED_NAME,
                params.PREVIOUS_PUBLICATION_YEAR,
            ],
        )
    )
    return pd.Series(
        {
            CONCERNS_RAISED_NAME: safeguarding_concerns_raised,
            YEAR_ON_YEAR_CONCERNS_RAISED_NAME: safeguarding_concerns_raised_proportion_growth,
        },
        name=params.PUBLICATION_YEAR,
    )


def calculate_new_requests_for_support_section(
    existing_time_series_data: pd.DataFrame, publications: Publications
) -> NewRequestsForSupport:
    new_requests_for_support_by_age = publications.ascfr.get_new_requests_by_age()
    new_requests_for_support_percent_growth_by_age = (
        calculate_new_requests_percent_growth_by_age(
            new_requests_for_support_by_age, existing_time_series_data
        )
    )
    return NewRequestsForSupport(
        new_requests_for_support_by_age,
        new_requests_for_support_percent_growth_by_age,
    )


def calculate_new_requests_percent_growth_by_age(
    new_requests_for_support_by_age: pd.Series, existing_time_series_data: pd.DataFrame
) -> pd.Series:
    new_requests_percent_growth_18_64 = calc_year_on_year_proportion_growth(
        new_requests_for_support_by_age.loc[
            params.NEW_REQUESTS_TABLE.ROW_NAMES.ASCFR_NEW_REQUESTS_18_64_NAME
        ],
        existing_time_series_data.loc[  # type: ignore
            params.NEW_REQUESTS_TABLE.ROW_NAMES.ASCFR_NEW_REQUESTS_18_64_NAME,
            params.PUBLICATION_YEAR_TO_COMPARE_GROWTH,
        ],
    )

    new_requests_percent_growth_65_plus = calc_year_on_year_proportion_growth(
        new_requests_for_support_by_age.loc[
            params.NEW_REQUESTS_TABLE.ROW_NAMES.ASCFR_NEW_REQUESTS_65_PLUS_NAME
        ],
        existing_time_series_data.loc[  # type: ignore
            params.NEW_REQUESTS_TABLE.ROW_NAMES.ASCFR_NEW_REQUESTS_65_PLUS_NAME,
            params.PUBLICATION_YEAR_TO_COMPARE_GROWTH,
        ],
    )
    return pd.Series(
        [new_requests_percent_growth_18_64, new_requests_percent_growth_65_plus],
        name=params.PUBLICATION_YEAR,
        index=[
            params.NEW_REQUESTS_TABLE.ROW_NAMES.ASCFR_GROWTH_18_64_SINCE_2015_16_NAME,
            params.NEW_REQUESTS_TABLE.ROW_NAMES.ASCFR_GROWTH_65_PLUS_SINCE_2015_16_NAME,
        ],
    )
