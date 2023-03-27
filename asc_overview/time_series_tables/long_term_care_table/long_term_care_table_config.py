from typed_params import BaseModel
from asc_overview.utilities.reindex_rows import get_row_order_from_row_names


class PrimarySupportReasonRowNames(BaseModel):
    PHYSICAL_SUPP_ACCESS_AND_MOBILITY: str
    PHYSICAL_SUPP_PERSONAL_CARE: str
    SENSORY_SUPP_VISUAL: str
    SENSORY_SUPP_HEARING: str
    SENSORY_SUPP_DUAL: str
    SUPP_WITH_MEMORY_AND_COGNITION: str
    LEARNING_DISABILITY_SUPP: str
    MENTAL_HEALTH_SUPP: str
    SOCIAL_SUPP_SUBSTANCE_MISUSE: str
    SOCIAL_SUPP_ASYLUM: str
    SOCIAL_SUPP_SOCIAL_ISOLATION: str


class LongTermCareRowNames(BaseModel):
    LONG_TERM_SUPPORT_18_64: str
    LONG_TERM_SUPPORT_65_PLUS: str
    POPULATION_18_64: str
    POPULATION_65_PLUS: str
    LONG_TERM_SUPPORT_PERCENT_18_64: str
    LONG_TERM_SUPPORT_PERCENT_65_PLUS: str
    NURSING_OR_RESIDENTIAL_18_64: str
    COMMUNITY_18_64: str
    NURSING_OR_RESIDENTIAL_65_PLUS: str
    COMMUNITY_65_PLUS: str
    PHYSICAL_SUPPORT_AS_PRIMARY_18_64: str
    OTHER_SUPPORT_AS_PRIMARY_18_64: str
    PHYSICAL_SUPPORT_AS_PRIMARY_65_PLUS: str
    OTHER_SUPPORT_AS_PRIMARY_65_PLUS: str


class LongTermCareTable(BaseModel):
    OVERVIEW_SHEET_NAME: str
    CELL_TO_WRITE_TO: str
    PRIMARY_SUPPORT_REASON_ROW_NAMES: PrimarySupportReasonRowNames
    ROW_NAMES: LongTermCareRowNames

    def get_row_order(self):
        return get_row_order_from_row_names(self.ROW_NAMES)
