import pandas as pd
from asc_overview import params
from asc_overview.utilities.load_from_excel import load_workbook_range_as_dataframe
from ..excel_publication_reader import ExcelPublicationReader


class AscfrReader(ExcelPublicationReader):
    def get_new_requests_by_age(self) -> pd.Series:
        df_new_requests_by_region = self.get_range_from_workbook_as_dataframe(
            params.ASCFR_LOADING_CONFIG.NEW_REQUESTS
        )

        region_by_new_requests = df_new_requests_by_region.T
        region_by_new_requests = (
            region_by_new_requests.set_axis(
                params.NEW_REQUESTS_TABLE.ASCFR_NEW_INDEX, axis="index"
            )
            .rename(columns={"England": params.PUBLICATION_YEAR})
            .squeeze()
        )

        return region_by_new_requests

    def get_completed_episodes_ST_Max_for_new_clients(self) -> pd.DataFrame:
        df_completed_episodes_st_max = self.get_range_from_workbook_as_dataframe(
            params.ASCFR_LOADING_CONFIG.NEW_CLIENTS
        ).drop(
            columns=params.SHORT_TERM_CARE_TABLE.COMPLETED_EPISODES_ST_MAX_COLUMNS_NEW_CLIENTS_TO_DROP
        )

        df_completed_episodes_st_max.columns = (
            df_completed_episodes_st_max.columns.str.replace("\n", " ").str.strip()
        )

        return df_completed_episodes_st_max.loc[
            params.SHORT_TERM_CARE_TABLE.COMPLETED_EPISODES_ST_MAX_ROWS
        ]

    def get_total_completed_episodes_ST_Max_for_existing_clients(self) -> pd.Series:
        df_completed_episodes_st_max = self.get_range_from_workbook_as_dataframe(
            params.ASCFR_LOADING_CONFIG.EXISTING_CLIENTS
        )

        return df_completed_episodes_st_max.loc[  # type: ignore
            params.SHORT_TERM_CARE_TABLE.COMPLETED_EPISODES_ST_MAX_ROWS, ["Total"]
        ]

    def get_long_term_support_by_support_setting(self) -> pd.DataFrame:
        df_support_setting_by_region = self.get_range_from_workbook_as_dataframe(
            params.ASCFR_LOADING_CONFIG.LONG_TERM_SUPPORT_SETTING_18_64
        )

        df_support_setting_by_region_18_64 = df_support_setting_by_region.iloc[
            :, :9
        ].rename({"England": "18 to 64"})
        df_support_setting_by_region_65_over = df_support_setting_by_region.iloc[
            :, 9:
        ].rename({"England": "65 and over"})

        return pd.concat(
            [df_support_setting_by_region_18_64, df_support_setting_by_region_65_over]
        ).rename(columns=lambda x: x.replace("\n", " ").strip())

    def get_primary_support_reason_18_64(self) -> pd.Series:
        return self.get_range_from_workbook_as_dataframe(
            params.ASCFR_LOADING_CONFIG.PRIMARY_SUPPORT_REASON_18_64
        ).pipe(self.format_df_total_primary_support_by_reason)

    def get_primary_support_reason_65_plus(self) -> pd.Series:
        return self.get_range_from_workbook_as_dataframe(
            params.ASCFR_LOADING_CONFIG.PRIMARY_SUPPORT_REASON_65_PLUS
        ).pipe(self.format_df_total_primary_support_by_reason)

    def format_df_total_primary_support_by_reason(
        self, df_total_primary_support_by_reason: pd.DataFrame
    ):
        return (
            df_total_primary_support_by_reason.squeeze()
            .set_axis(
                params.LONG_TERM_CARE_TABLE.PRIMARY_SUPPORT_REASON_ROW_NAMES.to_dict().values(),
                axis="index",
            )
            .rename(params.PUBLICATION_YEAR)
            .infer_objects()
        )

    def get_real_term_figures_by_year(self) -> pd.Series:
        return self.get_range_from_workbook_as_dataframe(
            params.ASCFR_LOADING_CONFIG.REAL_TERMS
        )["Real Terms"].rename(params.PUBLICATION_YEAR)

    def get_how_money_spent_figures_by_measure(self) -> pd.Series:
        HOW_MONEY_SPENT_COLUMNS = [
            "own_provision",
            "provision_by_others",
            "grants_voluntary_organisations",
            "total",
        ]

        return (
            self.get_range_from_workbook_as_dataframe(
                params.ASCFR_LOADING_CONFIG.HOW_MONEY_SPENT
            )
            .drop([params.PREVIOUS_PUBLICATION_YEAR], axis=1)
            .set_axis(HOW_MONEY_SPENT_COLUMNS, axis="columns")
            .T.squeeze()
            .rename(params.PUBLICATION_YEAR)
        )
