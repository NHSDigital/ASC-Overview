from typed_params import BaseModel
from asc_overview.utilities.excel_config import ExcelTableConfig
from asc_overview.utilities.reindex_rows import get_row_order_from_row_names


class NewRequestsRowNames(BaseModel):
    ASCFR_NEW_REQUESTS_18_64_NAME: str
    ASCFR_NEW_REQUESTS_65_PLUS_NAME: str
    ASCFR_GROWTH_18_64_SINCE_2015_16_NAME: str
    ASCFR_GROWTH_65_PLUS_SINCE_2015_16_NAME: str
    POPULATION_18_64: str
    POPULATION_65_PLUS: str
    NEW_REQUESTS_PER_POPULATION_18_64: str
    NEW_REQUESTS_PER_POPULATION_65_PLUS: str
    SAFEGUARDING_CONCERNS_RAISED_NAME: str
    DOLS_APPLICATIONS_RECEIVED_NAME: str
    SAFEGUARDING_YEAR_ON_YEAR_CONCERNS_RAISED_NAME: str
    DOLS_YEAR_ON_YEAR_APPLICATIONS_RECEIVED_NAME: str


class NewRequestsTable(BaseModel):
    OVERVIEW: ExcelTableConfig
    CELL_TO_WRITE_TO: str
    ROW_NAMES: NewRequestsRowNames
    ASCFR_NEW_INDEX: list[str]
    DOLS_APPLICATIONS_RECEIVED_ROW_NAME: str
    DOLS_APPLICATIONS_RECEIVED_COLUMN_NAME: str
    SAFEGUARDING_CONCERNS_RAISED_ROW_NAME: str
    SAFEGUARDING_CONCERNS_RAISED_COLUMN_NAME: str

    def get_row_order(self):
        return get_row_order_from_row_names(self.ROW_NAMES)
