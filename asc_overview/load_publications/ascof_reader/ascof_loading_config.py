from typed_params import BaseModel
from asc_overview.utilities.excel_config import ExcelWorkbookRange


class ExcelReferenceWithAge(BaseModel):
    SHEET_NAME: str
    CELL_REF_18_64: str
    CELL_REF_65_AND_OVER: str


class OutcomesByLa(BaseModel):
    SHEET_NAME: str
    RANGE_INDEX: ExcelWorkbookRange
    RANGE_18_64: ExcelWorkbookRange
    RANGE_65_AND_OVER: ExcelWorkbookRange


class AscofLoadingConfig(BaseModel):
    SERVICE_USER_SATISFACTION: ExcelReferenceWithAge
    CARER_SATISFACTION: ExcelReferenceWithAge
    SERVICE_USER_QUALITY_OF_LIFE: ExcelReferenceWithAge
    CARER_QUALITY_OF_LIFE: ExcelReferenceWithAge
    FEEL_SAFE_BY_AGE: ExcelReferenceWithAge
    SERVICE_USER_SOCIAL_CONTACT_BY_AGE: ExcelReferenceWithAge
    CARER_SOCIAL_CONTACT_BY_AGE: ExcelReferenceWithAge
    SOCIAL_CONTACT_BY_LA: OutcomesByLa
    FEEL_SAFE_BY_LA: OutcomesByLa
