import numpy as np
import pandas as pd
from asc_overview import params


def create_na_series_for_empty_row(row_name: str):
    return pd.Series({row_name: np.nan}, name=params.PUBLICATION_YEAR)
