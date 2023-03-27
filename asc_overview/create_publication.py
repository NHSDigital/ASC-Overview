from pathlib import Path
from openpyxl import load_workbook, Workbook
from asc_overview.load_publications.acfr_reader.ascfr_reader import AscfrReader
from asc_overview.load_publications.ascof_reader.ascof_reader import AscofReader
from asc_overview.load_publications.ascs_reader.ascs_reader import AscsReader
from asc_overview.load_publications.dols_reader.dols_reader import DolsReader
from asc_overview.load_publications.ons_reader import OnsReader
from asc_overview.load_publications.publications import Publications
from asc_overview.load_publications.safeguarding_reader.safeguarding_reader import (
    SafeguardingReader,
)
from asc_overview.load_publications.overview_reader.overview_reader import (
    OverviewReader,
)
from asc_overview.load_publications.workforce_reader.workforce_reader import (
    WorkforceReader,
)
from asc_overview.menu import choose_params, choose_to_download_publications
from asc_overview.input_data.download_publication import download_all_publications
from asc_overview.load_publications.load_publications import (
    load_ascfr_publication,
    load_ascof_workbook,
    load_ascs_publication,
    load_dols_data,
    load_overview_workbook,
    load_safeguarding_publication,
    load_workforce_publication,
)
from asc_overview.time_series_tables.la_expenditure_table.la_expenditure_table import (
    add_new_la_expenditure_time_series_column_to_workbook,
)
from asc_overview.time_series_tables.long_term_care_table.long_term_care_table import (
    add_new_long_term_care_time_series_column_to_workbook,
)
from asc_overview.time_series_tables.new_requests_table.new_requests_table import (
    add_new_requests_time_series_column_to_workbook,
)
from asc_overview import params
from asc_overview.time_series_tables.short_term_care.short_term_care_table import (
    add_new_short_term_care_time_series_column_to_workbook,
)
from asc_overview.time_series_tables.social_care_experience_table.social_care_experience_table import (
    add_new_social_care_experience_time_series_column_to_workbook,
)
from asc_overview.time_series_tables.outcomes_table.outcomes_table import (
    add_new_outcomes_time_series_column_to_workbook,
)
from asc_overview.time_series_tables.more_outcomes_table.more_outcomes_table import (
    add_new_more_outcomes_time_series_column_to_workbook,
)
from asc_overview.la_breakdown_tables.outcomes_by_la_table.outcomes_by_la_table import (
    add_outcomes_by_la_to_workbook,
)
from asc_overview.time_series_tables.workforce_table.workforce_table import (
    add_new_workforce_time_series_column_to_workbook,
)
from asc_overview.cms_tables.cms_tables import (
    output_all_cms_tables,
)
from asc_overview.graphs.generate_scatter import generate_scatter_plot
from asc_overview import OUTPUT_TIME_SERIES_FILENAME


def create_publications_object() -> Publications:
    ascfr_reader = AscfrReader(load_ascfr_publication())
    ascof_reader = AscofReader(load_ascof_workbook())
    ascs_reader = AscsReader(load_ascs_publication())
    dols_reader = DolsReader(load_dols_data())
    safeguarding_reader = SafeguardingReader(load_safeguarding_publication())
    workforce_reader = WorkforceReader(load_workforce_publication())

    return Publications(
        ascfr=ascfr_reader,
        ascof=ascof_reader,
        ascs=ascs_reader,
        dols=dols_reader,
        safeguarding=safeguarding_reader,
        ons=OnsReader(),
        workforce=workforce_reader,
    )


def output_time_series_tables_to_workbook(
    template_workbook: Workbook, publications: Publications
) -> None:
    add_new_requests_time_series_column_to_workbook(template_workbook, publications)
    add_new_short_term_care_time_series_column_to_workbook(
        template_workbook, publications
    )
    add_new_long_term_care_time_series_column_to_workbook(
        template_workbook, publications
    )
    add_new_la_expenditure_time_series_column_to_workbook(
        template_workbook, publications
    )
    add_new_social_care_experience_time_series_column_to_workbook(
        template_workbook, publications
    )
    add_new_outcomes_time_series_column_to_workbook(template_workbook, publications)
    add_new_more_outcomes_time_series_column_to_workbook(
        template_workbook, publications
    )
    add_outcomes_by_la_to_workbook(template_workbook, publications)
    add_new_workforce_time_series_column_to_workbook(template_workbook, publications)


def save_outputs(template_workbook: Workbook):
    template_workbook.save(
        str(Path(params.PATH_TO_OUTPUTS) / OUTPUT_TIME_SERIES_FILENAME)
    )

    overview_reader = OverviewReader(load_overview_workbook())
    output_all_cms_tables(overview_reader, params.PATH_TO_OUTPUTS)
    generate_scatter_plot(overview_reader)


def main() -> None:
    choose_params()
    if choose_to_download_publications():
        download_all_publications()
    template_workbook = load_workbook(f"./{params.ASC_OVERVIEW_TEMPLATE_FILE_NAME}")

    publications = create_publications_object()

    output_time_series_tables_to_workbook(template_workbook, publications)
    try:
        save_outputs(template_workbook)
    except PermissionError as err:
        raise PermissionError(
            f"Output could not be saved! You may have the output file open: {err.filename}"
        )


if __name__ == "__main__":
    main()
