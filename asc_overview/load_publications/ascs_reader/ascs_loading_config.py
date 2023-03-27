from typed_params import BaseModel
from asc_overview.utilities.excel_config import ExcelTableConfig, ExcelCellConfig


class AscsLoadingConfig(BaseModel):
    SERVICE_USERS_FEELINGS_THEMSELVES: ExcelTableConfig
    SERVICE_USERS_FEELINGS_CHOICE: ExcelTableConfig
