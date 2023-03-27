from typed_params import BaseModel


class ExcelWorkbookRange(BaseModel):
    CELL_START: str
    CELL_END: str


class ExcelTableConfig(BaseModel):
    SHEET_NAME: str
    WORKBOOK_RANGE: ExcelWorkbookRange


class ExcelDisconnectedTableConfig(BaseModel):
    SHEET_NAME: str
    INDEX_WORKBOOK_RANGE: ExcelWorkbookRange
    COLUMN_WORKBOOK_RANGE: ExcelWorkbookRange
    DATA_WORKBOOK_RANGE: ExcelWorkbookRange


class ExcelCellConfig(BaseModel):
    SHEET_NAME: str
    CELL_REF: str
