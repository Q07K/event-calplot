"""Main API for creating calendar heatmaps."""

from typing import Literal

import pandas as pd
import plotly.graph_objs as go

from .layout import calculate_month_positions, create_layout
from .preprocessing import filter_by_year, get_years_in_data, preprocess_data
from .traces import (
    add_event_markers,
    calculate_month_line_positions,
    create_event_heatmap_trace,
    create_month_separator_traces,
    create_value_heatmap_trace,
)


def create_calendar_heatmap(
    data: pd.DataFrame,
    date_col: str,
    value_col: str,
    year: int,
    language: Literal["en", "ko"] = "en",
    min_color: str = "#eeeeee",
    max_color: str = "#678fae",
    line_color: str = "#9e9e9e",
    line_width: float = 1.5,
    hover_template: str | None = None,
    event_dates: list[pd.Timestamp] | None = None,
    event_color: str = "#76cf61",
) -> go.Figure:
    """Create a calendar heatmap visualization.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing date and value columns
    date_col : str
        Name of the date column
    value_col : str
        Name of the value column
    year : int
        Year to visualize
    language : Literal["en", "ko"], optional
        Language for labels ('en' or 'ko'), by default "en"
    min_color : str, optional
        Color for minimum values, by default "#eeeeee"
    max_color : str, optional
        Color for maximum values, by default "#678fae"
    line_color : str, optional
        Color for month separator lines, by default "#9e9e9e"
    line_width : float, optional
        Width of month separator lines, by default 1.5
    hover_template : str | None, optional
        Custom hover template (None for default), by default None
    event_dates : list[pd.Timestamp] | None, optional
        List of dates to highlight as events (None for no events), by default None
    event_color : str, optional
        Color for event markers, by default "#76cf61"

    Returns
    -------
    go.Figure
        Figure object for the calendar heatmap

    Raises
    ------
    ValueError
        If specified year is not in the data

    Examples
    --------
    >>> import pandas as pd
    >>> from event_calplot import create_calendar_heatmap
    >>> df = pd.DataFrame({
    ...     'date': pd.date_range('2023-01-01', '2023-12-31'),
    ...     'value': range(365)
    ... })
    >>> fig = create_calendar_heatmap(
    ...     data=df,
    ...     date_col='date',
    ...     value_col='value',
    ...     year=2023
    ... )
    >>> fig.show()
    """
    # Preprocess data
    processed_data = preprocess_data(
        df=data,
        date_col=date_col,
        value_col=value_col,
    )

    # Validate year
    available_years = get_years_in_data(df=processed_data, date_col=date_col)
    if year not in available_years:
        raise ValueError(
            f"Year {year} not found in data. "
            f"Available years: {available_years}"
        )

    # Filter to specified year
    year_data = filter_by_year(df=processed_data, date_col=date_col, year=year)

    # Add event markers if provided
    if event_dates is not None:
        year_data = add_event_markers(
            df=year_data,
            event_dates=event_dates,
            date_col=date_col,
        )

    # Calculate month positions for layout
    days_in_months = (
        year_data[date_col]
        .dt.to_period(freq="M")
        .unique()
        .days_in_month.tolist()
    )
    month_positions = calculate_month_positions(days_in_months=days_in_months)

    # Create layout
    layout = create_layout(month_positions=month_positions, language=language)

    # Calculate month line positions
    year_data = calculate_month_line_positions(df=year_data, date_col=date_col)

    # Create traces
    traces: list[go.Scatter | go.Heatmap] = []

    # Month separator lines
    line_traces = create_month_separator_traces(
        df=year_data,
        color=line_color,
        line_width=line_width,
    )
    traces.extend(line_traces)

    # Value heatmap
    value_trace = create_value_heatmap_trace(
        df=year_data,
        date_col=date_col,
        value_col=value_col,
        min_color=min_color,
        max_color=max_color,
        hover_template=hover_template,
    )
    traces.append(value_trace)

    # Event overlay (if events are present)
    if event_dates is not None:
        event_trace = create_event_heatmap_trace(
            df=year_data,
            color=event_color,
        )
        traces.append(event_trace)

    # Create figure
    fig = go.Figure(data=traces, layout=layout)
    fig.update_layout(
        title={
            "text": str(year),
            "x": 0.5,
            "xanchor": "center",
        },
    )

    return fig


# def create_multi_year_heatmap(
#     data: pd.DataFrame,
#     date_col: str,
#     value_col: str,
#     language: Literal["en", "ko"] = "en",
#     **kwargs,
# ) -> list[go.Figure]:
#     """
#     Create calendar heatmaps for all years in the data.

#     Args:
#         data: DataFrame containing date and value columns
#         date_col: Name of the date column
#         value_col: Name of the value column
#         language: Language for labels ('en' or 'ko')
#         **kwargs: Additional arguments passed to create_calendar_heatmap

#     Returns:
#         List of Plotly Figure objects, one per year

#     Example:
#         >>> import pandas as pd
#         >>> from calendar_heatmap import create_multi_year_heatmap
#         >>>
#         >>> df = pd.DataFrame({
#         ...     'date': pd.date_range('2023-01-01', '2024-12-31'),
#         ...     'value': range(731)
#         ... })
#         >>>
#         >>> figures = create_multi_year_heatmap(
#         ...     data=df,
#         ...     date_col='date',
#         ...     value_col='value'
#         ... )
#         >>> for fig in figures:
#         ...     fig.show()
#     """
#     # Preprocess data
#     processed_data = preprocess_data(
#         df=data, date_col=date_col, value_col=value_col
#     )

#     # Get all years
#     years = get_years_in_data(df=processed_data, date_col=date_col)

#     # Create figure for each year
#     figures = []
#     for year in years:
#         fig = create_calendar_heatmap(
#             data=processed_data,
#             date_col=date_col,
#             value_col=value_col,
#             year=year,
#             language=language,
#             **kwargs,
#         )
#         fig.update_layout(
#             title={
#                 "text": str(year),
#                 "x": 0.5,
#                 "xanchor": "center",
#             },
#         )
#         figures.append(fig)

#     return figures
