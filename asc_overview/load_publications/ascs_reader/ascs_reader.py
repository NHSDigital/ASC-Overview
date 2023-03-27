import pandas as pd
from asc_overview import params
from asc_overview.utilities.format_series_as_percentage import (
    format_series_as_percentage,
)
from ..excel_publication_reader import ExcelPublicationReader


class AscsReader(ExcelPublicationReader):
    def get_service_user_feelings_themselves(self) -> pd.Series:
        SOCIAL_CARE_EXPERIENCE_ROW_NAMES = params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES

        df_service_user_feelings_by_region = self.get_range_from_workbook_as_dataframe(
            params.ASCS_LOADING_CONFIG.SERVICE_USERS_FEELINGS_THEMSELVES,
        )
        return (
            df_service_user_feelings_by_region.iloc[:, :4]
            .squeeze()
            .set_axis(
                [
                    SOCIAL_CARE_EXPERIENCE_ROW_NAMES.FEEL_BETTER_ABOUT_SELF,
                    SOCIAL_CARE_EXPERIENCE_ROW_NAMES.DOES_NOT_AFFECT_SELF,
                    SOCIAL_CARE_EXPERIENCE_ROW_NAMES.SOMETIMES_UNDERMINES_SELF,
                    SOCIAL_CARE_EXPERIENCE_ROW_NAMES.COMPLETELY_UNDERMINES_SELF,
                ]
            )
            .infer_objects()
            .rename(params.PUBLICATION_YEAR)
            .pipe(format_series_as_percentage)
        )

    def get_service_user_feelings_choice(self):
        SOCIAL_CARE_EXPERIENCE_ROW_NAMES = params.SOCIAL_CARE_EXPERIENCE_TABLE.ROW_NAMES

        df_service_user_feelings_by_region = self.get_range_from_workbook_as_dataframe(
            params.ASCS_LOADING_CONFIG.SERVICE_USERS_FEELINGS_CHOICE
        )
        return (
            df_service_user_feelings_by_region.iloc[:, :3]
            .squeeze()
            .set_axis(
                [
                    SOCIAL_CARE_EXPERIENCE_ROW_NAMES.HAVE_ENOUGH_CHOICE,
                    SOCIAL_CARE_EXPERIENCE_ROW_NAMES.DONT_HAVE_ENOUGH_CHOICE,
                    SOCIAL_CARE_EXPERIENCE_ROW_NAMES.DONT_WANT_CHOICE,
                ]
            )
            .infer_objects()
            .rename(params.PUBLICATION_YEAR)
            .pipe(format_series_as_percentage)
        )
