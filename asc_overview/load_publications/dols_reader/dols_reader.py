from asc_overview import params
from ..excel_publication_reader import ExcelPublicationReader


class DolsReader(ExcelPublicationReader):
    def get_applications_received(self) -> int:
        return self.get_cell_from_workbook(params.DOLS_LOADING_CONFIG.NEW_REQUESTS)
