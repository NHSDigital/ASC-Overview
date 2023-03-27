from typing import Optional
import requests
from asc_overview import params

PATH_TO_DOWNLOADED_PUBLICATIONS = "./asc_overview/input_data/"


def download_publication(
    url: str,
    publication_filename: str,
    path_to_downloaded_publications: Optional[str] = None,
) -> None:
    if path_to_downloaded_publications is None:
        path_to_downloaded_publications = PATH_TO_DOWNLOADED_PUBLICATIONS

    response = requests.get(url, verify=False)
    with open(
        f"{path_to_downloaded_publications}/{publication_filename}", "wb"
    ) as output_file:
        output_file.write(response.content)


def download_all_publications():
    for publication_file in params.PUBLICATIONS.to_dict().values():
        download_publication(
            publication_file.URL,
            publication_file.FILENAME,
        )
