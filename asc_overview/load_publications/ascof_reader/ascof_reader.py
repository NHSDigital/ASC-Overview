import pandas as pd
from asc_overview import params
from asc_overview.utilities.load_from_excel import (
    load_workbook_cell,
    load_workbook_column,
)
from asc_overview.utilities.format_series_as_percentage import (
    format_series_as_percentage,
)
from asc_overview.load_publications.ascof_reader.ascof_loading_config import (
    ExcelReferenceWithAge,
    OutcomesByLa,
)
from ..excel_publication_reader import ExcelPublicationReader


class AscofReader(ExcelPublicationReader):
    def create_age_series_from_config(
        self, excel_reference_with_age: ExcelReferenceWithAge
    ) -> pd.Series:
        worksheet = self.get_sheet_from_worbook(excel_reference_with_age.SHEET_NAME)

        value_18_64 = load_workbook_cell(
            excel_reference_with_age.CELL_REF_18_64, worksheet
        )

        value_65_and_over = load_workbook_cell(
            excel_reference_with_age.CELL_REF_65_AND_OVER, worksheet
        )

        return pd.Series(
            {"18 to 64": value_18_64, "65 and over": value_65_and_over},
            name=params.PUBLICATION_YEAR,
        )

    def get_service_user_percentage_satisfaction_by_age(self) -> pd.Series:
        return self.create_age_series_from_config(
            params.ASCOF_LOADING_CONFIG.SERVICE_USER_SATISFACTION
        ).pipe(format_series_as_percentage)

    def get_service_user_quality_of_life_score_by_age(self) -> pd.Series:
        return self.create_age_series_from_config(
            params.ASCOF_LOADING_CONFIG.SERVICE_USER_QUALITY_OF_LIFE
        )

    def get_carer_percentage_satisfaction_by_age(self) -> pd.Series:
        """
        The carers information is only published every 2 years,
        so we want to only load that data when it is available (represented by the param).
        """
        if params.LOAD_CARERS_DATA:
            try:
                return self._get_carer_percentage_satisfaction()
            except KeyError:
                raise AssertionError("No carers data found!")
        else:
            carer_percentage_satisfaction_index = [
                params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES.CARER_SATISFACTION_18_64,
                params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES.CARER_SATISFACTION_65_AND_OVER,
            ]
            return self.get_na_carer_series(carer_percentage_satisfaction_index)

    def get_carer_quality_of_life_score_by_age(self) -> pd.Series:
        if params.LOAD_CARERS_DATA:
            try:
                return self._get_carer_quality_of_life()
            except KeyError:
                raise AssertionError("No carers data found!")
        else:
            carer_quality_of_life_score_index = ["18 to 64", "65 and over"]
            return self.get_na_carer_series(carer_quality_of_life_score_index)

    def get_carer_social_contact_by_age(self) -> pd.Series:
        if params.LOAD_CARERS_DATA:
            try:
                return self._get_carer_social_contact()
            except KeyError:
                raise AssertionError("No carers data found!")
        else:
            carer_social_contact_index = ["18 to 64", "65 and over"]
            return self.get_na_carer_series(carer_social_contact_index)

    def _get_carer_social_contact(self) -> pd.Series:

        return self.create_age_series_from_config(
            params.ASCOF_LOADING_CONFIG.CARER_SOCIAL_CONTACT_BY_AGE
        ).pipe(format_series_as_percentage)

    def get_na_carer_series(self, index: list[str]):
        return pd.Series(
            ["N/A", "N/A"],
            index=index,
            name=params.PUBLICATION_YEAR,
        )

    def _get_carer_percentage_satisfaction(self) -> pd.Series:
        return self.create_age_series_from_config(
            params.ASCOF_LOADING_CONFIG.CARER_SATISFACTION
        ).pipe(format_series_as_percentage)

    def _get_carer_quality_of_life(self) -> pd.Series:

        return self.create_age_series_from_config(
            params.ASCOF_LOADING_CONFIG.CARER_QUALITY_OF_LIFE
        )

    def get_service_user_safety(self) -> pd.Series:

        return self.create_age_series_from_config(
            params.ASCOF_LOADING_CONFIG.FEEL_SAFE_BY_AGE
        ).pipe(format_series_as_percentage)

    def get_service_user_social_contact_by_age(self) -> pd.Series:

        return self.create_age_series_from_config(
            params.ASCOF_LOADING_CONFIG.SERVICE_USER_SOCIAL_CONTACT_BY_AGE
        ).pipe(format_series_as_percentage)

    def create_age_dataframe_from_config(
        self, outcomes_by_la: OutcomesByLa
    ) -> pd.DataFrame:
        worksheet = self.get_sheet_from_worbook(outcomes_by_la.SHEET_NAME)

        outcomes_by_la_index = load_workbook_column(
            outcomes_by_la.RANGE_INDEX, worksheet
        ).rename("la_index")
        outcomes_by_la_18_64 = load_workbook_column(
            outcomes_by_la.RANGE_18_64, worksheet
        ).rename("18 to 64")
        outcomes_by_la_65_and_over = load_workbook_column(
            outcomes_by_la.RANGE_65_AND_OVER, worksheet
        ).rename("65 and over")

        return pd.concat(
            [outcomes_by_la_index, outcomes_by_la_18_64, outcomes_by_la_65_and_over],
            axis=1,
        ).set_index("la_index")

    def get_service_user_socal_contact_by_la(self) -> pd.DataFrame:
        return self.create_age_dataframe_from_config(
            params.ASCOF_LOADING_CONFIG.SOCIAL_CONTACT_BY_LA
        )

    def get_service_user_feel_safe_by_la(self) -> pd.DataFrame:
        return self.create_age_dataframe_from_config(
            params.ASCOF_LOADING_CONFIG.FEEL_SAFE_BY_LA
        )
