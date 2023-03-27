from openpyxl import Workbook
import pandas as pd
from asc_overview.load_publications.ons_reader import OnsReader
from asc_overview import params
from asc_overview.load_publications.publications import Publications
from asc_overview.utilities.output_to_excel import output_time_series_column_to_workbook
from asc_overview.utilities.reindex_rows import (
    reindex_rows,
)
from asc_overview.utilities.output_to_excel import get_worksheet_from_workbook


def add_new_long_term_care_time_series_column_to_workbook(
    template_workbook: Workbook, publications: Publications
) -> None:
    long_term_care_sheet = get_worksheet_from_workbook(
        template_workbook, params.LONG_TERM_CARE_TABLE.OVERVIEW_SHEET_NAME
    )

    new_time_series_column = create_new_time_series_column(publications)

    output_time_series_column_to_workbook(
        long_term_care_sheet,
        new_time_series_column,
        params.LONG_TERM_CARE_TABLE.CELL_TO_WRITE_TO,
    )


def create_new_time_series_column(publications: Publications) -> pd.Series:
    long_term_support_by_setting = (
        publications.ascfr.get_long_term_support_by_support_setting()
    )
    population_data_by_age = get_population_data_by_age(publications.ons)
    long_term_support_proportion_by_age = calculate_long_term_support_proportion_by_age(
        long_term_support_by_setting, population_data_by_age
    )
    primary_support_reason_18_64 = publications.ascfr.get_primary_support_reason_18_64()
    primary_support_reason_65_plus = (
        publications.ascfr.get_primary_support_reason_65_plus()
    )

    long_term_support_by_age = calculate_total_long_term_support(
        long_term_support_by_setting
    )
    nursing_and_residential_by_age = calculate_nursing_and_residential(
        long_term_support_by_setting
    )
    community_care_by_age = calculate_community_care(long_term_support_by_setting)

    physical_as_primary_support_by_age = calculate_physical_as_primary_support(
        primary_support_reason_18_64, primary_support_reason_65_plus
    )
    other_primary_support_reason_by_age = calculate_other_primary_support_reason(
        primary_support_reason_18_64, primary_support_reason_65_plus
    )

    return (
        pd.concat(
            [
                long_term_support_by_age,
                population_data_by_age,
                long_term_support_proportion_by_age,
                nursing_and_residential_by_age,
                community_care_by_age,
                physical_as_primary_support_by_age,
                other_primary_support_reason_by_age,
            ]
        )
        .pipe(reindex_rows, params.LONG_TERM_CARE_TABLE.get_row_order())
        .round(3)
    )


def calculate_total_long_term_support(
    long_term_support_by_setting: pd.DataFrame,
) -> pd.Series:
    return (
        long_term_support_by_setting["Total"]
        .rename(
            {
                "18 to 64": params.LONG_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT_18_64,
                "65 and over": params.LONG_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT_65_PLUS,
            },
            axis="index",
        )
        .rename(params.PUBLICATION_YEAR)
    )


def get_population_data_by_age(ons_reader: OnsReader) -> pd.Series:
    population_data_18_64 = ons_reader.get_population_data_18_64()
    population_data_65_plus = ons_reader.get_population_data_65_plus()

    return pd.Series(
        {
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.POPULATION_18_64: population_data_18_64,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.POPULATION_65_PLUS: population_data_65_plus,
        },
        name=params.PUBLICATION_YEAR,
    )


def calculate_long_term_support_proportion_by_age(
    long_term_support_by_setting: pd.DataFrame, population_data_by_age: pd.Series
) -> pd.Series:
    print(population_data_by_age)
    long_term_support_proportion_18_64 = (
        long_term_support_by_setting.loc["18 to 64", "Total"]
        / population_data_by_age.loc[
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.POPULATION_18_64
        ]
    )

    long_term_support_proportion_65_plus = (
        long_term_support_by_setting.loc["65 and over", "Total"]
        / population_data_by_age.loc[
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.POPULATION_65_PLUS
        ]
    )

    return pd.Series(
        {
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT_PERCENT_18_64: long_term_support_proportion_18_64,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT_PERCENT_65_PLUS: long_term_support_proportion_65_plus,
        },
        name=params.PUBLICATION_YEAR,
    )


def calculate_nursing_and_residential(
    long_term_support_by_setting: pd.DataFrame,
) -> pd.Series:
    return (
        (
            long_term_support_by_setting["Nursing"]
            + long_term_support_by_setting["Residential"]
        )
        .squeeze()
        .rename(  # type: ignore
            {
                "18 to 64": params.LONG_TERM_CARE_TABLE.ROW_NAMES.NURSING_OR_RESIDENTIAL_18_64,
                "65 and over": params.LONG_TERM_CARE_TABLE.ROW_NAMES.NURSING_OR_RESIDENTIAL_65_PLUS,
            },
            axis="index",
        )
        .rename(params.PUBLICATION_YEAR)
    )


def calculate_community_care(long_term_support_by_setting: pd.DataFrame) -> pd.Series:
    COLUMNS_TO_SUM_FOR_COMMUNITY_CARE = [
        "Community Direct Payment Only",
        "Community Part Direct Payment",
        "Community CASSR Managed Personal Budget",
        "Community CASSR Commissioned Support Only",
        "Prison CASSR Managed Personal Budget",
        "Prison CASSR Commissioned Support Only",
    ]

    return (
        long_term_support_by_setting[COLUMNS_TO_SUM_FOR_COMMUNITY_CARE]
        .sum(axis=1)
        .squeeze()
        .rename(  # type: ignore
            {
                "18 to 64": params.LONG_TERM_CARE_TABLE.ROW_NAMES.COMMUNITY_18_64,
                "65 and over": params.LONG_TERM_CARE_TABLE.ROW_NAMES.COMMUNITY_65_PLUS,
            }
        )
        .rename(params.PUBLICATION_YEAR)
    )


def calculate_physical_as_primary_support(
    primary_support_reason_18_64: pd.Series, primary_support_reason_65_plus: pd.Series
) -> pd.Series:
    physical_as_primary_support_18_64 = (
        primary_support_reason_18_64[
            params.LONG_TERM_CARE_TABLE.PRIMARY_SUPPORT_REASON_ROW_NAMES.PHYSICAL_SUPP_ACCESS_AND_MOBILITY
        ]
        + primary_support_reason_18_64[
            params.LONG_TERM_CARE_TABLE.PRIMARY_SUPPORT_REASON_ROW_NAMES.PHYSICAL_SUPP_PERSONAL_CARE
        ]
    )
    physical_as_primary_support_65_plus = (
        primary_support_reason_65_plus[
            params.LONG_TERM_CARE_TABLE.PRIMARY_SUPPORT_REASON_ROW_NAMES.PHYSICAL_SUPP_ACCESS_AND_MOBILITY
        ]
        + primary_support_reason_65_plus[
            params.LONG_TERM_CARE_TABLE.PRIMARY_SUPPORT_REASON_ROW_NAMES.PHYSICAL_SUPP_PERSONAL_CARE
        ]
    )

    return pd.Series(
        [physical_as_primary_support_18_64, physical_as_primary_support_65_plus],
        index=[
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.PHYSICAL_SUPPORT_AS_PRIMARY_18_64,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.PHYSICAL_SUPPORT_AS_PRIMARY_65_PLUS,
        ],
        name=params.PUBLICATION_YEAR,
    )


def calculate_other_primary_support_reason(
    primary_support_reason_18_64: pd.Series, primary_support_reason_65_plus: pd.Series
) -> pd.Series:
    COLUMNS_TO_SUM_FOR_OTHER_PRIMARY_SUPPORT_REASON = [
        "Sensory Support: Support for Visual Impairment",
        "Sensory Support: Support for Hearing Impairment",
        "Sensory Support: Support for Dual Impairment",
        "Support with Memory and Cognition",
        "Learning Disability Support",
        "Mental Health Support",
        "Social Support: Substance Misuse Support",
        "Social Support: Asylum Seeker Support",
        "Social Support: Support for Social Isolation/Other",
    ]

    other_primary_support_reason_18_64 = primary_support_reason_18_64[
        COLUMNS_TO_SUM_FOR_OTHER_PRIMARY_SUPPORT_REASON
    ].sum()

    other_primary_support_reason_65_plus = primary_support_reason_65_plus[
        COLUMNS_TO_SUM_FOR_OTHER_PRIMARY_SUPPORT_REASON
    ].sum()

    return pd.Series(
        [other_primary_support_reason_18_64, other_primary_support_reason_65_plus],
        index=[
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.OTHER_SUPPORT_AS_PRIMARY_18_64,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.OTHER_SUPPORT_AS_PRIMARY_65_PLUS,
        ],
        name=params.PUBLICATION_YEAR,
    )
