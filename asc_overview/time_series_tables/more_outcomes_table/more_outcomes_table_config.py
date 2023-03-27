from typed_params import BaseModel
from asc_overview.utilities.reindex_rows import get_row_order_from_row_names


class MoreOutcomesRowNames(BaseModel):
    SERVICE_USER_SAFETY_18_64: str
    SERVICE_USER_SAFETY_65_AND_OVER: str
    SERVICE_USER_SOCIAL_CONTACT_18_64: str
    SERVICE_USER_SOCIAL_CONTACT_65_AND_OVER: str
    CARERS_SOCIAL_CONTACT_18_64: str
    CARERS_SOCIAL_CONTACT_65_AND_OVER: str


class MoreOutcomesTable(BaseModel):
    OVERVIEW_SHEET_NAME: str
    CELL_TO_WRITE_TO: str
    ROW_NAMES: MoreOutcomesRowNames

    def get_row_order(self):
        return get_row_order_from_row_names(self.ROW_NAMES)
