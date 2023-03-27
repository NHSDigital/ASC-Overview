from typed_params import BaseModel
from typing import Union
from asc_overview.utilities.reindex_rows import get_row_order_from_row_names


class ShortTermCareRowNames(BaseModel):
    TOTAL_COMPLETED_EPISODES_18_64: str
    TOTAL_COMPLETED_EPISODES_65_PLUS: str
    WHAT_HAPPENED_NEXT: str
    EARLY_CESSATION_OF_SERVICE: str
    LONG_TERM_SUPPORT: str
    ONGOING_LOW_LEVEL_SUPPORT: str
    SHORT_TERM_SUPPORT: str
    NO_SERVICES_DECLINED: str
    NO_SERVICES_UNVERSAL_SIGNPOSTED: str
    NO_SERVICES_NO_IDENTIFIED: str
    PERCENT_EARLY_CESSATION: str
    PERCENT_LONG_TERM_SUPPORT: str
    PERCENT_ONGOING_LOW_LEVEL_SUPPORT: str
    PERCENT_SHORT_TERM_SUPPORT: str
    PERCENT_NO_SERVICES_DECLINED: str
    PERCENT_NO_SERVICES_UNVERSAL_SIGNPOSTED: str
    PERCENT_NO_SERVICES_NO_IDENTIFIED: str


class CompletedEpisodesStMaxColumnNames(BaseModel):
    EARLY_CESSATION_OF_SERVICE_NHS_FUNDED_COLUMN_NAME: str
    EARLY_CESSATION_OF_SERVICE_COLUMN_NAME: str
    EARLY_CESSATION_OF_SERVICE_LONG_TERM_SUPPORT: str
    LONG_TERM_SUPPORT: str
    ONGOING_LOW_LEVEL_SUPPORT: str
    SHORT_TERM_SUPPORT: str
    NO_SERVICES_SELF_FUNDING: str
    NO_SERVICES_DECLINED: str
    NO_SERVICES_UNVERSAL_SIGNPOSTED: str
    NO_SERVICES_NO_IDENTIFIED: str


class ShortTermCareTable(BaseModel):
    OVERVIEW_SHEET_NAME: str
    COMPLETED_EPISODES_ST_MAX_ROWS: list[str]
    COMPLETED_EPISODES_ST_MAX_COLUMNS_NEW_CLIENTS_TO_DROP: list[Union[str, None]]
    COMPLETED_EPISODES_ST_MAX_COLUMNS_EXISTING_CLIENTS_TO_DROP: list[Union[str, None]]
    COMPLETED_EPISODES_ST_MAX_COLUMN_NAMES: CompletedEpisodesStMaxColumnNames
    CELL_TO_WRITE_TO: str
    ROW_NAMES: ShortTermCareRowNames

    def get_row_order(self):
        return get_row_order_from_row_names(self.ROW_NAMES)

    def get_measure_names(self) -> list[str]:
        return [
            value
            for key, value in self.ROW_NAMES.to_dict().items()
            if "TOTAL" not in key
            and "PERCENT" not in key
            and "WHAT_HAPPENED_NEXT" not in key
        ]
