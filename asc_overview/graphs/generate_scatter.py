from typing import NamedTuple
from asc_overview.load_publications.overview_reader.overview_reader import (
    OverviewReader,
)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import pandas as pd
import numpy as np
from asc_overview import params
from sklearn.linear_model import LinearRegression

CHART_COLOR_18_64 = "#005EB8"
CHART_COLOR_65_AND_OVER = "#919EA8"


class MeasureByAge(NamedTuple):
    age_18_64: pd.Series
    age_65_and_over: pd.Series


class AgeMeasures(NamedTuple):
    social_contact: MeasureByAge
    feel_safe: MeasureByAge


def generate_scatter_plot(overview_reader: OverviewReader):
    age_measures = get_age_measures(overview_reader)

    social_contact = age_measures.social_contact
    feel_safe = age_measures.feel_safe

    fig, ax = setup_figure()

    plot_data_for_age_measure(
        ax,
        social_contact.age_18_64,
        feel_safe.age_18_64,
        colour=CHART_COLOR_18_64,
        label="18-64",
    )
    plot_data_for_age_measure(
        ax,
        social_contact.age_65_and_over,
        feel_safe.age_65_and_over,
        colour=CHART_COLOR_65_AND_OVER,
        label="65 and over",
    )

    fig.legend(bbox_to_anchor=(0.5, -0.15), loc="center", ncol=4, frameon=False)

    fig.savefig(
        f"{params.PATH_TO_OUTPUTS}/social contact and feelings of safety.png",
        bbox_inches="tight",
        dpi=300,
    )


def get_age_measures(overview_reader: OverviewReader) -> AgeMeasures:
    outcomes_by_la = overview_reader.outcomes_by_la_table
    outcomes_by_la.columns = pd.MultiIndex.from_product(
        [["social_contact", "feel_safe"], ["18_64", "65_and_over"]]
    )
    social_contact_18_64 = get_measure_by_age(outcomes_by_la, "social_contact", "18_64")
    social_contact_65_and_over = get_measure_by_age(
        outcomes_by_la, "social_contact", "65_and_over"
    )

    feel_safe_18_64 = get_measure_by_age(outcomes_by_la, "feel_safe", "18_64")
    feel_safe_65_and_over = get_measure_by_age(
        outcomes_by_la, "feel_safe", "65_and_over"
    )

    social_contact = MeasureByAge(social_contact_18_64, social_contact_65_and_over)
    feel_safe = MeasureByAge(feel_safe_18_64, feel_safe_65_and_over)

    return AgeMeasures(social_contact, feel_safe)


def setup_figure() -> tuple[Figure, Axes]:
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    set_figure_labels(ax)
    format_figure(ax)
    return fig, ax


def plot_data_for_age_measure(
    axes: Axes, social_contact: pd.Series, feel_safe: pd.Series, colour: str, label: str
):
    axes.scatter(social_contact, feel_safe, color=colour, label=label)

    maximum_point, minimum_point = calculate_line_of_best_fit(social_contact, feel_safe)

    plot_line_of_best_fit(
        maximum_point, minimum_point, colour, f"Linear ({label})", axes
    )


def plot_line_of_best_fit(
    maximum_point: np.ndarray,
    minimum_point: np.ndarray,
    color: str,
    label: str,
    axes: Axes,
):
    axes.plot(
        maximum_point,
        minimum_point,
        color=color,
        label=label,
        linestyle="dotted",
    )


def calculate_line_of_best_fit(
    age_measure_1: pd.Series, age_measure_2: pd.Series
) -> tuple[np.ndarray, np.ndarray]:
    FORWARD_FORECAST_AMOUNT = 10
    BACKWORD_FORECAST_AMOUNT = 5
    regression_model = LinearRegression()
    regression_model.fit(age_measure_1.values.reshape(-1, 1), age_measure_2)
    forward_forecast_x = age_measure_1.max() + FORWARD_FORECAST_AMOUNT
    forward_forecast_y = regression_model.predict(
        np.array(forward_forecast_x).reshape(-1, 1)
    )
    backward_forecast_x = age_measure_1.min() - BACKWORD_FORECAST_AMOUNT
    backward_forecast_y = regression_model.predict(
        np.array(backward_forecast_x).reshape(-1, 1)
    )

    maximum_point = np.append(backward_forecast_x, forward_forecast_x)
    minimum_point = np.append(backward_forecast_y, forward_forecast_y)

    return maximum_point, minimum_point


def set_figure_labels(axes: Axes):
    axes.set_xlabel(
        "% of people who use services in each local authority who reported that they had as much social contact as they would like",
        wrap=True,
    )
    axes.set_ylabel(
        "% of people who use services in each local authority who feel safe"
    )
    axes.set_title("Social contact and feelings of safety")


def format_figure(axes: Axes):
    axes.set_xlim(0, 100)
    axes.set_ylim(0, 100)
    axes.grid(b=True)


def get_measure_by_age(
    outcomes_by_la: pd.DataFrame, measure: str, age_band: str
) -> pd.Series:
    return outcomes_by_la[(measure, age_band)].pipe(
        format_measure_by_age_for_scatter_plot
    )


def format_measure_by_age_for_scatter_plot(measure_by_age: pd.Series):
    return measure_by_age.replace("[x]", np.nan).dropna()
