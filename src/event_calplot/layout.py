"""Layout utilities for the calendar plot."""

from typing import Literal

import numpy as np
import plotly.graph_objects as go

from .locales import get_locale_text


def calculate_month_positions(days_in_months: list[int]) -> list[float]:
    """Calculate x-axis positions for month labels.

    Parameters
    ----------
    days_in_months : list[int]
        List of days in each month

    Returns
    -------
    list[float]
        List of positions (in weeks) for month labels
    """

    MID_MONTH_DAY = (
        15  # Subtract 15 to position the label at the middle of the month
    )
    cumsum = np.cumsum(days_in_months)
    return ((cumsum - MID_MONTH_DAY) / 7).tolist()


def create_layout(
    month_positions: list[float],
    language: Literal["en", "ko"] = "en",
) -> go.Layout:
    """Create a Plotly layout for the calendar plot.

    Parameters
    ----------
    month_positions : list[float]
        List of positions (in weeks) for month labels
    language : Literal["en", "ko"], optional
        Language for the layout, by default "en"

    Returns
    -------
    go.Layout
        Plotly layout for the calendar plot
    """

    locale_text = get_locale_text(language=language)
    months = locale_text["months"]
    weekdays = locale_text["weekdays"]

    return go.Layout(
        height=250,
        yaxis={
            "showline": False,
            "showgrid": False,
            "zeroline": False,
            "tickmode": "array",
            "ticktext": weekdays,
            "tickvals": [0, 1, 2, 3, 4, 5, 6],
            "autorange": "reversed",
            "tickfont": {"size": 12, "color": "#9e9e9e"},
        },
        xaxis={
            "showline": False,
            "showgrid": False,
            "zeroline": False,
            "tickmode": "array",
            "ticktext": months,
            "tickvals": month_positions,
            "tickfont": {"size": 12, "color": "#9e9e9e"},
        },
        plot_bgcolor="white",
        margin={"t": 40},
        showlegend=False,
    )
