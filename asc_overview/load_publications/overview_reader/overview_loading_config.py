from typed_params import BaseModel
from asc_overview.utilities.excel_config import ExcelTableConfig


class OverviewLoadingConfig(BaseModel):
    NEW_REQUESTS: ExcelTableConfig
    SHORT_TERM_CARE: ExcelTableConfig
    LONG_TERM_CARE: ExcelTableConfig
    LA_EXPENDITURE: ExcelTableConfig
    PROPORTION_LA_EXPENDITURE: ExcelTableConfig
    WORKFORCE: ExcelTableConfig
    SOCIAL_CARE_EXPERIENCE: ExcelTableConfig
    SOCIAL_CARE_EXPERIENCE_CHOICE: ExcelTableConfig
    OUTCOMES: ExcelTableConfig
    MORE_OUTCOMES: ExcelTableConfig
    OUTCOMES_BY_LA: ExcelTableConfig
