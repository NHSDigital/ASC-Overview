from asc_overview.params_utils.params import get_params_from_file


OUTPUT_TIME_SERIES_FILENAME = "output.xlsx"
STARTUP_PARAMS_FILE = "./params_json/2021-22.json"


params = get_params_from_file(STARTUP_PARAMS_FILE)
