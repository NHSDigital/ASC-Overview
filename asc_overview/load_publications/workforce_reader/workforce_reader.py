import pandas as pd
from ..excel_publication_reader import ExcelPublicationReader
from .workforce_loading_config import JOB_ROLES, JOB_ROLE_BREAKDOWNS
from asc_overview import params


class WorkforceReader(ExcelPublicationReader):
    def get_all_job_roles(self) -> pd.Series:
        df_job_roles_by_region = self.get_range_from_workbook_as_dataframe(
            params.WORKFORCE_LOADING_CONFIG.ALL_JOB_ROLES,
        ).set_axis(
            pd.MultiIndex.from_product([JOB_ROLES, JOB_ROLE_BREAKDOWNS]),
            axis=1,
        )

        return (
            df_job_roles_by_region.loc["England"]
            .rename(params.PUBLICATION_YEAR)
            .infer_objects()
        )

    def get_new_starters(self) -> int:
        return self.get_cell_from_workbook(params.WORKFORCE_LOADING_CONFIG.NEW_STARTERS)

    def get_leavers(self) -> int:
        return self.get_cell_from_workbook(params.WORKFORCE_LOADING_CONFIG.LEAVERS)
