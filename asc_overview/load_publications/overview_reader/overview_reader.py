from typing import cast
import numpy as np
import pandas as pd
from openpyxl import Workbook
from asc_overview import params
from asc_overview.utilities.format_series_as_percentage import (
    format_percentage_as_number,
)
from ..excel_publication_reader import ExcelPublicationReader

ALL_YEARS = [
    "2015-16",
    "2016-17",
    "2017-18",
    "2018-19",
    "2019-20",
    "2020-21",
]
YEARS_WITHOUT_2015 = ["2016-17", "2017-18", "2018-19", "2019-20", "2020-21"]


class OverviewReader(ExcelPublicationReader):
    def __init__(self, wb: Workbook) -> None:
        super().__init__(wb)
        self.setup_table_dataframes()

    def setup_table_dataframes(self) -> None:
        self.new_requests_table = self.get_range_from_workbook_as_dataframe(
            params.OVERVIEW_LOADING_CONFIG.NEW_REQUESTS
        )

        self.short_term_care_table = self.get_range_from_workbook_as_dataframe(
            params.OVERVIEW_LOADING_CONFIG.SHORT_TERM_CARE
        )

        self.long_term_care_table = self.get_range_from_workbook_as_dataframe(
            params.OVERVIEW_LOADING_CONFIG.LONG_TERM_CARE
        )

        self.la_expenditure_table = self.get_range_from_workbook_as_dataframe(
            params.OVERVIEW_LOADING_CONFIG.LA_EXPENDITURE
        )

        self.workforce_table = self.get_range_from_workbook_as_dataframe(
            params.OVERVIEW_LOADING_CONFIG.WORKFORCE
        )

        self.social_care_experience_table = self.get_range_from_workbook_as_dataframe(
            params.OVERVIEW_LOADING_CONFIG.SOCIAL_CARE_EXPERIENCE
        )

        self.outcomes_table = self.get_range_from_workbook_as_dataframe(
            params.OVERVIEW_LOADING_CONFIG.OUTCOMES
        )

        self.more_outcomes_table = self.get_range_from_workbook_as_dataframe(
            params.OVERVIEW_LOADING_CONFIG.MORE_OUTCOMES
        )

        self.outcomes_by_la_table = self.get_range_from_workbook_as_dataframe(
            params.OVERVIEW_LOADING_CONFIG.OUTCOMES_BY_LA
        )

    def get_new_requests_for_support(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.NEW_REQUESTS_TABLE.ROW_NAMES.ASCFR_NEW_REQUESTS_18_64_NAME,
            params.NEW_REQUESTS_TABLE.ROW_NAMES.ASCFR_NEW_REQUESTS_65_PLUS_NAME,
        ]

        return self.new_requests_table.loc[ROWS_REQUIRED].pipe(
            self.transpose_and_infer_objects
        )

    def get_change_in_requests(self) -> pd.DataFrame:
        ROWS_REQURED = [
            params.NEW_REQUESTS_TABLE.ROW_NAMES.ASCFR_GROWTH_18_64_SINCE_2015_16_NAME,
            params.NEW_REQUESTS_TABLE.ROW_NAMES.ASCFR_GROWTH_65_PLUS_SINCE_2015_16_NAME,
        ]
        return self.new_requests_table.loc[ROWS_REQURED, YEARS_WITHOUT_2015].pipe(
            self.transpose_and_infer_objects
        )

    def get_new_requests_per_population(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.NEW_REQUESTS_TABLE.ROW_NAMES.NEW_REQUESTS_PER_POPULATION_18_64,
            params.NEW_REQUESTS_TABLE.ROW_NAMES.NEW_REQUESTS_PER_POPULATION_65_PLUS,
        ]

        return self.new_requests_table.loc[ROWS_REQUIRED].pipe(
            self.transpose_and_infer_objects
        )

    def get_dols_requests(self) -> pd.Series:
        return cast(
            pd.Series,
            self.new_requests_table.loc[
                params.NEW_REQUESTS_TABLE.ROW_NAMES.DOLS_APPLICATIONS_RECEIVED_NAME
            ].pipe(self.transpose_and_infer_objects),
        )

    def get_safeguarding_requests(self) -> pd.Series:

        return cast(
            pd.Series,
            self.new_requests_table.loc[
                params.NEW_REQUESTS_TABLE.ROW_NAMES.SAFEGUARDING_CONCERNS_RAISED_NAME,
                YEARS_WITHOUT_2015,
            ].pipe(self.transpose_and_infer_objects),
        )

    def get_change_in_safeguarding_and_dols(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.NEW_REQUESTS_TABLE.ROW_NAMES.SAFEGUARDING_YEAR_ON_YEAR_CONCERNS_RAISED_NAME,
            params.NEW_REQUESTS_TABLE.ROW_NAMES.DOLS_YEAR_ON_YEAR_APPLICATIONS_RECEIVED_NAME,
        ]
        return (
            self.new_requests_table.loc[ROWS_REQUIRED, YEARS_WITHOUT_2015]
            .T.replace("N/A", np.nan)
            .infer_objects()
        )

    def get_short_term_support(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.TOTAL_COMPLETED_EPISODES_18_64,
            params.SHORT_TERM_CARE_TABLE.ROW_NAMES.TOTAL_COMPLETED_EPISODES_65_PLUS,
        ]

        return self.short_term_care_table.loc[ROWS_REQUIRED].pipe(
            self.transpose_and_infer_objects
        )

    def get_percent_what_happened_next(self) -> pd.DataFrame:
        ROW_NAMES = params.SHORT_TERM_CARE_TABLE.ROW_NAMES
        ROWS_REQUIRED = [
            ROW_NAMES.PERCENT_EARLY_CESSATION,
            ROW_NAMES.PERCENT_LONG_TERM_SUPPORT,
            ROW_NAMES.PERCENT_ONGOING_LOW_LEVEL_SUPPORT,
            ROW_NAMES.PERCENT_SHORT_TERM_SUPPORT,
            ROW_NAMES.PERCENT_NO_SERVICES_DECLINED,
            ROW_NAMES.PERCENT_NO_SERVICES_UNVERSAL_SIGNPOSTED,
            ROW_NAMES.PERCENT_NO_SERVICES_NO_IDENTIFIED,
        ]

        return cast(
            pd.DataFrame,
            self.short_term_care_table.loc[ROWS_REQUIRED]
            .pipe(self.transpose_and_infer_objects)
            .pipe(format_percentage_as_number),
        )

    def get_long_term_support_per_population(self) -> pd.DataFrame:
        ROWS_REQURIED = [
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT_PERCENT_18_64,
            params.LONG_TERM_CARE_TABLE.ROW_NAMES.LONG_TERM_SUPPORT_PERCENT_65_PLUS,
        ]

        return cast(
            pd.DataFrame,
            self.long_term_care_table.loc[ROWS_REQURIED]
            .pipe(self.transpose_and_infer_objects)
            .apply(format_percentage_as_number),
        )

    def get_long_term_support_setting(self) -> pd.DataFrame:
        ROW_NAMES = params.LONG_TERM_CARE_TABLE.ROW_NAMES
        ROWS_REQUIRED = [
            ROW_NAMES.NURSING_OR_RESIDENTIAL_18_64,
            ROW_NAMES.COMMUNITY_18_64,
            ROW_NAMES.NURSING_OR_RESIDENTIAL_65_PLUS,
            ROW_NAMES.COMMUNITY_65_PLUS,
        ]

        return self.long_term_care_table.loc[ROWS_REQUIRED].pipe(
            self.transpose_and_infer_objects
        )

    def get_primary_support_reason(self) -> pd.DataFrame:
        ROW_NAMES = params.LONG_TERM_CARE_TABLE.ROW_NAMES
        ROWS_REQUIRED = [
            ROW_NAMES.PHYSICAL_SUPPORT_AS_PRIMARY_18_64,
            ROW_NAMES.OTHER_SUPPORT_AS_PRIMARY_18_64,
            ROW_NAMES.PHYSICAL_SUPPORT_AS_PRIMARY_65_PLUS,
            ROW_NAMES.OTHER_SUPPORT_AS_PRIMARY_65_PLUS,
        ]

        return self.long_term_care_table.loc[ROWS_REQUIRED].pipe(
            self.transpose_and_infer_objects
        )

    def get_gross_current_expenditure(self) -> pd.Series:
        return cast(
            pd.Series,
            self.la_expenditure_table.loc[
                params.LA_EXPENDITURE_TABLE.ROW_NAMES.GROSS_CURRENT_EXPENDITURE
            ].pipe(self.transpose_and_infer_objects),
        )

    def get_expenditure_per_citizen(self) -> pd.Series:
        return cast(
            pd.Series,
            self.la_expenditure_table.loc[
                params.LA_EXPENDITURE_TABLE.ROW_NAMES.GROSS_CURRENT_EXPENDITURE_PER_ADULT
            ].pipe(self.transpose_and_infer_objects),
        )

    def get_proportion_la_expenditure(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.PERCENT_LA_OWN_PROVISION,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.PERCENT_PROVISION_BY_OTHERS,
            params.LA_EXPENDITURE_TABLE.ROW_NAMES.PERCENT_GRANTS_TO_VOLUNTARY_ORGANISATIONS,
        ]
        return cast(
            pd.DataFrame,
            self.la_expenditure_table.loc[ROWS_REQUIRED]
            .dropna(axis=1)
            .apply(format_percentage_as_number)
            .pipe(self.transpose_and_infer_objects),
        )

    def get_jobs(self) -> pd.Series:
        return cast(
            pd.Series,
            self.workforce_table.loc[params.WORKFORCE_TABLE.ROW_NAMES.JOBS]
            .pipe(self.transpose_and_infer_objects)
            .rename(int)
            .rename(index=self.append_end_sept_to_row_names),
        )

    def get_vacancies(self) -> pd.Series:
        return cast(
            pd.Series,
            self.workforce_table.loc[params.WORKFORCE_TABLE.ROW_NAMES.VACANCIES]
            .pipe(self.transpose_and_infer_objects)
            .rename(int)
            .rename(index=self.append_end_sept_to_row_names),
        )

    def get_starters_and_leavers(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.WORKFORCE_TABLE.ROW_NAMES.NEW_STARTERS,
            params.WORKFORCE_TABLE.ROW_NAMES.LEAVERS,
        ]

        return (
            self.workforce_table.loc[ROWS_REQUIRED]
            .pipe(self.transpose_and_infer_objects)
            .rename(int)
        )

    def get_job_role(self) -> pd.DataFrame:
        ROW_NAMES = params.WORKFORCE_TABLE.ROW_NAMES
        ROWS_REQUIRED = [
            ROW_NAMES.PERCENT_DIRECT_CARE,
            ROW_NAMES.PERCENT_MANAGER_SUPERVISOR,
            ROW_NAMES.PERCENT_PROFESSIONAL,
            ROW_NAMES.PERCENT_OTHER,
        ]

        return cast(
            pd.DataFrame,
            self.workforce_table.loc[ROWS_REQUIRED]
            .pipe(self.transpose_and_infer_objects)
            .apply(format_percentage_as_number)
            .rename(int)
            .rename(index=self.append_end_sept_to_row_names),
        )

    def get_service_user_satisfaction(self) -> pd.DataFrame:
        ROW_NAMES = params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES
        ROWS_REQUIRED = [
            ROW_NAMES.SERVICE_USER_SATISFACTION_18_64,
            ROW_NAMES.SERVICE_USER_SATISFACTION_65_AND_OVER,
        ]

        return cast(
            pd.DataFrame,
            self.social_care_experience_table.loc[ROWS_REQUIRED]
            .pipe(self.transpose_and_infer_objects)
            .apply(format_percentage_as_number),
        )

    def get_service_user_feelings_themselves(self) -> pd.DataFrame:
        ROW_NAMES = params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES
        ROWS_REQUIRED = [
            ROW_NAMES.FEEL_BETTER_ABOUT_SELF,
            ROW_NAMES.DOES_NOT_AFFECT_SELF,
            ROW_NAMES.SOMETIMES_UNDERMINES_SELF,
            ROW_NAMES.COMPLETELY_UNDERMINES_SELF,
        ]

        return cast(
            pd.DataFrame,
            self.social_care_experience_table.loc[ROWS_REQUIRED]
            .pipe(self.transpose_and_infer_objects)
            .apply(format_percentage_as_number),
        )

    def get_service_user_feelings_choice(self) -> pd.DataFrame:
        ROW_NAMES = params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES
        ROWS_REQUIRED = [
            ROW_NAMES.HAVE_ENOUGH_CHOICE,
            ROW_NAMES.DONT_HAVE_ENOUGH_CHOICE,
            ROW_NAMES.DONT_WANT_CHOICE,
        ]

        return cast(
            pd.DataFrame,
            self.social_care_experience_table.loc[ROWS_REQUIRED]
            .dropna(axis=1)
            .pipe(self.transpose_and_infer_objects)
            .apply(format_percentage_as_number),
        )

    def get_carer_satisfaction(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES.CARER_SATISFACTION_18_64,
            params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES.CARER_SATISFACTION_65_AND_OVER,
        ]

        return cast(
            pd.DataFrame,
            self.social_care_experience_table.loc[ROWS_REQUIRED]
            .T.pipe(self.drop_years_when_carer_data_is_na)
            .infer_objects()
            .apply(format_percentage_as_number),
        )

    def get_service_user_quality_of_life(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.OUTCOMES_TABLE.ROW_NAMES.SERVICE_USER_QUALITY_OF_LIFE_18_64,
            params.OUTCOMES_TABLE.ROW_NAMES.SERVICE_USER_QUALITY_OF_LIFE_65_AND_OVER,
        ]

        return self.outcomes_table.loc[ROWS_REQUIRED].pipe(
            self.transpose_and_infer_objects
        )

    def get_carer_quality_of_life(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.OUTCOMES_TABLE.ROW_NAMES.CARER_QUALITY_OF_LIFE_18_64,
            params.OUTCOMES_TABLE.ROW_NAMES.CARER_QUALITY_OF_LIFE_65_AND_OVER,
        ]

        return (
            self.outcomes_table.loc[ROWS_REQUIRED]
            .T.pipe(self.drop_years_when_carer_data_is_na)
            .infer_objects()
        )

    def get_safeguarding_enquiries(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.OUTCOMES_TABLE.ROW_NAMES.PERCENT_FULLY_ACHIEVED,
            params.OUTCOMES_TABLE.ROW_NAMES.PERCENT_FULLY_OR_PARTLY_ACHIEVED,
        ]

        return cast(
            pd.DataFrame,
            self.outcomes_table.loc[ROWS_REQUIRED]
            .T.dropna()
            .infer_objects()
            .apply(format_percentage_as_number),
        )

    def get_service_user_feelings_safety(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.MORE_OUTCOMES_TABLE.ROW_NAMES.SERVICE_USER_SAFETY_18_64,
            params.MORE_OUTCOMES_TABLE.ROW_NAMES.SERVICE_USER_SAFETY_65_AND_OVER,
        ]

        return cast(
            pd.DataFrame,
            self.more_outcomes_table.loc[ROWS_REQUIRED]
            .pipe(self.transpose_and_infer_objects)
            .apply(format_percentage_as_number),
        )

    def get_service_user_social_contact(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.MORE_OUTCOMES_TABLE.ROW_NAMES.SERVICE_USER_SOCIAL_CONTACT_18_64,
            params.MORE_OUTCOMES_TABLE.ROW_NAMES.SERVICE_USER_SOCIAL_CONTACT_65_AND_OVER,
        ]

        return cast(
            pd.DataFrame,
            self.more_outcomes_table.loc[ROWS_REQUIRED]
            .pipe(self.transpose_and_infer_objects)
            .apply(format_percentage_as_number),
        )

    def get_carer_social_contact(self) -> pd.DataFrame:
        ROWS_REQUIRED = [
            params.MORE_OUTCOMES_TABLE.ROW_NAMES.CARERS_SOCIAL_CONTACT_18_64,
            params.MORE_OUTCOMES_TABLE.ROW_NAMES.CARERS_SOCIAL_CONTACT_65_AND_OVER,
        ]

        return cast(
            pd.DataFrame,
            self.more_outcomes_table.loc[ROWS_REQUIRED]
            .T.pipe(self.drop_years_when_carer_data_is_na)
            .infer_objects()
            .apply(format_percentage_as_number),
        )

    def transpose_and_infer_objects(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return cast(pd.DataFrame, dataframe.T.infer_objects())

    def drop_years_when_carer_data_is_na(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe.replace("N/A", np.nan).dropna()

    def append_end_sept_to_row_names(self, row_name: str) -> str:
        return f"end Sept {row_name}"
