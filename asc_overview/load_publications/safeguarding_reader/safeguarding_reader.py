import pandas as pd
from asc_overview import params
from ..excel_publication_reader import ExcelPublicationReader


class SafeguardingReader(ExcelPublicationReader):
    def get_concerns_raised(self) -> int:
        return self.get_cell_from_workbook(
            params.SAFEGUARDING_LOADING_CONFIG.NEW_REQUESTS
        )

    def get_safeguarding_outcomes(self) -> pd.Series:
        OUTCOMES_COLUMNS = ["Fully Achieved", "Partially Achieved", "Not Achieved"]

        df_safeguarding_outcomes_by_region = self.get_range_from_workbook_as_dataframe(
            params.SAFEGUARDING_LOADING_CONFIG.OUTCOMES
        )

        return (
            df_safeguarding_outcomes_by_region.loc["England", OUTCOMES_COLUMNS]
            .infer_objects()
            .T.rename(params.PUBLICATION_YEAR)  # type: ignore
        )

    def get_concerns_raised_by_region(self) -> pd.Series:
        return (
            self.get_disconnected_dataframe_from_workbook(
                params.SAFEGUARDING_LOADING_CONFIG.CONCERNS_BY_REGION
            )
            .squeeze()
            .rename(params.PUBLICATION_YEAR)
            .infer_objects()
        )
