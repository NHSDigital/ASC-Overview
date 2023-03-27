import os
from typing import Optional
from asc_overview import params
from asc_overview.input_data.download_publication import (
    download_publication,
    download_all_publications,
)


def test_download_publication(tmp_path):
    publication_to_download_name = "test.xlsx"

    publications_in_download_directory_before_download = os.listdir(tmp_path)

    assert (
        publication_to_download_name
        not in publications_in_download_directory_before_download
    )

    download_publication(
        params.PUBLICATIONS.ASCFR.URL,
        publication_to_download_name,
        tmp_path,
    )

    publications_in_download_directory_after_download = os.listdir(tmp_path)

    assert (
        publication_to_download_name
        in publications_in_download_directory_after_download
    )


def test_download_all_publications(mocker):
    def mocked_download_publication(
        url: str,
        publication_filename: str,
        path_to_downloaded_publications: Optional[str] = None,
    ):
        return

    mocked_download_publication = mocker.patch(
        "asc_overview.input_data.download_publication.download_publication",
        side_effect=mocked_download_publication,
    )

    download_all_publications()

    mocked_download_publication.assert_called()
    assert mocked_download_publication.call_count == len(
        params.PUBLICATIONS.to_dict().values()
    )
