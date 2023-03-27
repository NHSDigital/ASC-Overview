from typed_params import BaseModel
from asc_overview.utilities.excel_config import (
    ExcelCellConfig,
    ExcelDisconnectedTableConfig,
    ExcelTableConfig,
)


class SafeguardingLoadingConfig(BaseModel):
    NEW_REQUESTS: ExcelCellConfig
    OUTCOMES: ExcelTableConfig
    CONCERNS_BY_REGION: ExcelDisconnectedTableConfig
