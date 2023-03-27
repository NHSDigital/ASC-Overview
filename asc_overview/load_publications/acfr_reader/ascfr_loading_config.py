from typed_params import BaseModel
from asc_overview.utilities.excel_config import ExcelTableConfig


class AscfrLoadingConfig(BaseModel):
    LONG_TERM_SUPPORT_SETTING_18_64: ExcelTableConfig
    PRIMARY_SUPPORT_REASON_18_64: ExcelTableConfig
    PRIMARY_SUPPORT_REASON_65_PLUS: ExcelTableConfig
    NEW_CLIENTS: ExcelTableConfig
    EXISTING_CLIENTS: ExcelTableConfig
    NEW_REQUESTS: ExcelTableConfig
    REAL_TERMS: ExcelTableConfig
    HOW_MONEY_SPENT: ExcelTableConfig
