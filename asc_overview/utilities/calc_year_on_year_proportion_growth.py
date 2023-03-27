def calc_year_on_year_proportion_growth(
    latest_year_data: int, previous_year_data: int
) -> float:
    return (latest_year_data - previous_year_data) / previous_year_data
