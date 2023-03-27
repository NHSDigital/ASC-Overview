from typed_params import BaseModel
from asc_overview.utilities.reindex_rows import get_row_order_from_row_names


class LaExpenditureRowNames(BaseModel):
    GROSS_CURRENT_EXPENDITURE: str
    ADULT_POPULATION: str
    GROSS_CURRENT_EXPENDITURE_PER_ADULT: str
    HOW_MONEY_SPENT: str
    LA_OWN_PROVISION: str
    PROVISION_BY_OTHERS: str
    GRANTS_TO_VOLUNTARY_ORGANISATIONS: str
    PERCENT_LA_OWN_PROVISION: str
    PERCENT_PROVISION_BY_OTHERS: str
    PERCENT_GRANTS_TO_VOLUNTARY_ORGANISATIONS: str


class LaExpenditureTable(BaseModel):
    OVERVIEW_SHEET_NAME: str
    CELL_TO_WRITE_TO: str
    ROW_NAMES: LaExpenditureRowNames

    def get_row_order(self):
        return get_row_order_from_row_names(self.ROW_NAMES)
