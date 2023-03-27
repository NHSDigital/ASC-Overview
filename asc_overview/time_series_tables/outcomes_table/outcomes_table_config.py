from typed_params import BaseModel
from asc_overview.utilities.reindex_rows import get_row_order_from_row_names


class OutcomesRowNames(BaseModel):
    SERVICE_USER_QUALITY_OF_LIFE_18_64: str
    SERVICE_USER_QUALITY_OF_LIFE_65_AND_OVER: str
    CARER_QUALITY_OF_LIFE_18_64: str
    CARER_QUALITY_OF_LIFE_65_AND_OVER: str
    DELAYED_TRANSFERS: str
    DELAYED_TRANSFERS_AND_ATTRIBUTABLE: str
    FULLY_ACHIEVED: str
    PARTLY_ACHIEVED: str
    NOT_ACHIEVED: str
    PERCENT_FULLY_ACHIEVED: str
    PERCENT_PARTLY_ACHIEVED: str
    PERCENT_FULLY_OR_PARTLY_ACHIEVED: str


class OutcomesTable(BaseModel):
    OVERVIEW_SHEET_NAME: str
    CELL_TO_WRITE_TO: str
    ROW_NAMES: OutcomesRowNames

    def get_row_order(self):
        return get_row_order_from_row_names(self.ROW_NAMES)
