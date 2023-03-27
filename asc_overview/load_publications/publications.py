from typing import NamedTuple

from asc_overview.load_publications.acfr_reader.ascfr_reader import AscfrReader
from asc_overview.load_publications.ascof_reader.ascof_reader import AscofReader
from asc_overview.load_publications.ascs_reader.ascs_reader import AscsReader
from asc_overview.load_publications.dols_reader.dols_reader import DolsReader
from asc_overview.load_publications.safeguarding_reader.safeguarding_reader import (
    SafeguardingReader,
)
from asc_overview.load_publications.workforce_reader.workforce_reader import (
    WorkforceReader,
)
from asc_overview.load_publications.ons_reader import OnsReader


class Publications(NamedTuple):
    ascfr: AscfrReader
    ascof: AscofReader
    ascs: AscsReader
    dols: DolsReader
    safeguarding: SafeguardingReader
    ons: OnsReader
    workforce: WorkforceReader
