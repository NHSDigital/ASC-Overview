from typed_params import BaseModel
from asc_overview.utilities.excel_config import ExcelTableConfig, ExcelCellConfig

JOB_ROLES = [
    "All job roles",
    "Direct care",
    "Manager / Supervisor",
    "Professional",
    "Other",
]

JOB_ROLE_BREAKDOWNS = ["Employees", "Vacancies"]


class WorkforceLoadingConfig(BaseModel):
    ALL_JOB_ROLES: ExcelTableConfig
    NEW_STARTERS: ExcelCellConfig
    LEAVERS: ExcelCellConfig
