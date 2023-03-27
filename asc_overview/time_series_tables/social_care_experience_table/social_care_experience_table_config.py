from typed_params import BaseModel
from asc_overview.utilities.reindex_rows import get_row_order_from_row_names


class SocialCareExperienceRowNames(BaseModel):
    SERVICE_USER_SATISFACTION_18_64: str
    SERVICE_USER_SATISFACTION_65_AND_OVER: str
    CARER_SATISFACTION_18_64: str
    CARER_SATISFACTION_65_AND_OVER: str
    SERVICE_USER_FEELINGS: str
    FEEL_BETTER_ABOUT_SELF: str
    DOES_NOT_AFFECT_SELF: str
    SOMETIMES_UNDERMINES_SELF: str
    COMPLETELY_UNDERMINES_SELF: str
    SERVICE_USERS_CHOICE: str
    HAVE_ENOUGH_CHOICE: str
    DONT_HAVE_ENOUGH_CHOICE: str
    DONT_WANT_CHOICE: str


class SocialCareExperienceTable(BaseModel):
    OVERVIEW_SHEET_NAME: str
    CELL_TO_WRITE_TO: str
    ROW_NAMES: SocialCareExperienceRowNames

    def get_row_order(self):
        return get_row_order_from_row_names(self.ROW_NAMES)
