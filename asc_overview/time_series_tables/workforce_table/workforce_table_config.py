from typed_params import BaseModel
from asc_overview.utilities.reindex_rows import get_row_order_from_row_names


class WorkforceRowNames(BaseModel):
    JOBS: str
    VACANCIES: str
    NEW_STARTERS: str
    LEAVERS: str
    TYPE_OF_ROLE: str
    DIRECT_CARE: str
    MANAGER_SUPERVISOR: str
    PROFESSIONAL: str
    OTHER: str
    PERCENT_DIRECT_CARE: str
    PERCENT_MANAGER_SUPERVISOR: str
    PERCENT_PROFESSIONAL: str
    PERCENT_OTHER: str


class WorkforceTable(BaseModel):
    OVERVIEW_SHEET_NAME: str
    CELL_TO_WRITE_TO: str
    ROW_NAMES: WorkforceRowNames

    def get_row_order(self):
        return get_row_order_from_row_names(self.ROW_NAMES)
