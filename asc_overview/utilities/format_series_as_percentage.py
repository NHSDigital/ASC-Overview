import pandas as pd


def format_series_as_percentage(series_to_format) -> pd.Series:
    return series_to_format / 100


def format_percentage_as_number(percentage_to_format) -> float:
    return percentage_to_format * 100
