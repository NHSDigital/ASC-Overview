import inquirer
import os
from asc_overview import params
from asc_overview.input_data.download_publication import PATH_TO_DOWNLOADED_PUBLICATIONS

PARAMS_DIRECTORY = "./params_json/"


def choose_params() -> None:
    params_files = [
        PARAMS_DIRECTORY + file
        for file in os.listdir(PARAMS_DIRECTORY)
        if file.endswith(".json")
    ]

    print("\nParams files available in params_json folder:\n")
    for i, file in enumerate(params_files):
        print(f"{i+1} - {file}")
    print()

    params_index_to_use = (
        int(inquirer.text(message="Enter the number of the params you wish to use")) - 1
    )
    params_file_to_use = params_files[params_index_to_use]

    params.set_params_from_params_json_file(params_file_to_use)


def choose_to_download_publications():
    publication_files = [
        file
        for file in os.listdir(PATH_TO_DOWNLOADED_PUBLICATIONS)
        if not file.startswith("~$") and file.endswith((".xlsx", ".xls"))
    ]

    if publication_files:
        print("\nPublication files downloaded:\n")
    else:
        print("\nNo publication files downloaded\n")
    for file in publication_files:
        print(file)
    print()
    return inquirer.confirm(
        "Do you want to download publications? (This will overwrite any existing files)",
        default=False,
    )
