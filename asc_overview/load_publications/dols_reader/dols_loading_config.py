from typed_params import BaseModel
from asc_overview.utilities.excel_config import ExcelCellConfig


class DolsLoadingConfig(BaseModel):
    NEW_REQUESTS: ExcelCellConfig
