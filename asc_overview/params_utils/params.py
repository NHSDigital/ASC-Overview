from typing import Union
from typed_params import BaseModel, load_params_dict_from_json_file
from pathlib import Path
from asc_overview.la_breakdown_tables.outcomes_by_la_table.outcomes_by_la_table_config import (
    OutcomesByLaTable,
)
from asc_overview.load_publications.ascs_reader.ascs_loading_config import (
    AscsLoadingConfig,
)
from asc_overview.load_publications.acfr_reader.ascfr_loading_config import (
    AscfrLoadingConfig,
)
from asc_overview.load_publications.ascof_reader.ascof_loading_config import (
    AscofLoadingConfig,
)
from asc_overview.load_publications.dols_reader.dols_loading_config import (
    DolsLoadingConfig,
)
from asc_overview.load_publications.safeguarding_reader.safeguarding_loading_config import (
    SafeguardingLoadingConfig,
)
from asc_overview.load_publications.overview_reader.overview_loading_config import (
    OverviewLoadingConfig,
)
from asc_overview.load_publications.workforce_reader.workforce_loading_config import (
    WorkforceLoadingConfig,
)
from asc_overview.time_series_tables.la_expenditure_table.la_expenditure_table_config import (
    LaExpenditureTable,
)
from asc_overview.time_series_tables.long_term_care_table.long_term_care_table_config import (
    LongTermCareTable,
)
from asc_overview.time_series_tables.more_outcomes_table.more_outcomes_table_config import (
    MoreOutcomesTable,
)
from asc_overview.time_series_tables.new_requests_table.new_requests_table_config import (
    NewRequestsTable,
)
from asc_overview.time_series_tables.outcomes_table.outcomes_table_config import (
    OutcomesTable,
)
from asc_overview.time_series_tables.short_term_care.short_term_care_table_config import (
    ShortTermCareTable,
)
from asc_overview.time_series_tables.social_care_experience_table.social_care_experience_table_config import (
    SocialCareExperienceTable,
)
from asc_overview.time_series_tables.workforce_table.workforce_table_config import (
    WorkforceTable,
)
import json


def get_params_from_file(file_path: Union[str, Path]):
    with open(file_path, encoding="UTF-8") as params_file:
        params_dict = json.load(params_file)

    return Params(params_dict)


class PublicationFile(BaseModel):
    NAME: str
    FILENAME: str
    URL: str


class PublicationModel(BaseModel):
    ASCFR: PublicationFile
    ASCOF: PublicationFile
    ASCS: PublicationFile
    DOLS_APPLICATIONS: PublicationFile
    SAFEGUARDING: PublicationFile
    WORKFORCE: PublicationFile
    ASC_OVERVIEW: PublicationFile


class Params(BaseModel):
    PUBLICATION_YEAR: str
    # Example: "2020-21"

    PREVIOUS_PUBLICATION_YEAR: str
    PUBLICATION_YEAR_TO_COMPARE_GROWTH: str

    ONS_POPULATION_YEAR: str
    # This year is used in the SQL query to get the correct year of ONS data

    WORKFORCE_YEAR: int
    # The Workforce table headings use a different convention to other tables
    # Example 2020

    LOAD_CARERS_DATA: bool

    PUBLICATIONS: PublicationModel
    PATH_TO_OUTPUTS: str
    ASC_OVERVIEW_TEMPLATE_FILE_NAME: str
    ASC_OVERVIEW_EXAMPLE_FILE_NAME: str

    NEW_REQUESTS_TABLE: NewRequestsTable
    SHORT_TERM_CARE_TABLE: ShortTermCareTable
    LONG_TERM_CARE_TABLE: LongTermCareTable
    LA_EXPENDITURE_TABLE: LaExpenditureTable
    WORKFORCE_TABLE: WorkforceTable
    SOCIAL_CARE_EXPERIENCE_TABLE: SocialCareExperienceTable
    OUTCOMES_TABLE: OutcomesTable
    MORE_OUTCOMES_TABLE: MoreOutcomesTable
    OUTCOMES_BY_LA_TABLE: OutcomesByLaTable

    ASCS_LOADING_CONFIG: AscsLoadingConfig
    ASCFR_LOADING_CONFIG: AscfrLoadingConfig
    ASCOF_LOADING_CONFIG: AscofLoadingConfig
    SAFEGUARDING_LOADING_CONFIG: SafeguardingLoadingConfig
    DOLS_LOADING_CONFIG: DolsLoadingConfig
    OVERVIEW_LOADING_CONFIG: OverviewLoadingConfig
    WORKFORCE_LOADING_CONFIG: WorkforceLoadingConfig
