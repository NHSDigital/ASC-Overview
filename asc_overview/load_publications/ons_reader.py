import pyodbc as dbc
from asc_overview import params

CONNECTION_STRING = """
    Driver=SQL Server;
    Server=DSSPROD;
    Database=DSS_CORPORATE;
    Trusted_Connection=yes;
"""


def get_population_query():
    return f"SELECT SUM(POPULATION_COUNT) FROM ONS_POPULATION_V2 WHERE YEAR_OF_COUNT = {params.ONS_POPULATION_YEAR} AND GEOGRAPHIC_GROUP_CODE = 'E12'"


class OnsReader:
    def __init__(self) -> None:
        self.connection = self.setup_database_connection()

    def setup_database_connection(self):
        return dbc.connect(CONNECTION_STRING)

    def get_population_data_18_64(self) -> int:
        return self.connection.execute(
            get_population_query() + " AND AGE_LOWER BETWEEN 18 AND 64"
        ).fetchone()[0]

    def get_population_data_65_plus(self) -> int:
        return self.connection.execute(
            get_population_query() + " AND AGE_LOWER > 64"
        ).fetchone()[0]
