"""Trace creation functions for calendar heatmap."""

import pandas as pd
import plotly.graph_objs as go


def calculate_month_line_positions(
    df: pd.DataFrame,
    date_col: str,
    line_offset: float = 0.5,
) -> pd.DataFrame:
    """Calculate positions for month separator lines.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with date and week information
    date_col : str
        Name of date column
    line_offset : float, optional
        Offset from grid cell border (0.5 = center of border), by default 0.5

    Returns
    -------
    pd.DataFrame
        DataFrame with line position columns added
    """
    result = df.copy()

    # Find first day of each month
    first_day_mask = result[date_col].dt.day == 1

    # First day that's not Monday (weekday != 0)
    not_monday_mask = result["weekday"] != 0
    combined_mask = first_day_mask & not_monday_mask

    # Vertical line at start of month
    result.loc[first_day_mask, "first_line_x"] = (
        result.loc[first_day_mask, "weeknum"] - line_offset
    )
    result.loc[first_day_mask, "first_line_y1"] = (
        result.loc[first_day_mask, "weekday"] - line_offset
    )
    result.loc[first_day_mask, "first_line_y2"] = 6 + line_offset

    # Horizontal line at top of month (when month starts mid-week)
    result.loc[combined_mask, "second_line_x1"] = (
        result.loc[combined_mask, "weeknum"] - line_offset
    )
    result.loc[combined_mask, "second_line_x2"] = (
        result.loc[combined_mask, "weeknum"] + line_offset
    )
    result.loc[combined_mask, "second_line_y"] = (
        result.loc[combined_mask, "weekday"] - line_offset
    )

    # Vertical line from top to month start (when month starts mid-week)
    result.loc[combined_mask, "third_line_x"] = (
        result.loc[combined_mask, "weeknum"] + line_offset
    )
    result.loc[combined_mask, "third_line_y1"] = (
        result.loc[combined_mask, "weekday"] - line_offset
    )
    result.loc[combined_mask, "third_line_y2"] = -line_offset

    return result


def create_month_separator_traces(
    df: pd.DataFrame,
    color: str = "#9e9e9e",
    line_width: float = 1.5,
) -> tuple[go.Scatter, go.Scatter, go.Scatter]:
    """Create month separator traces.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with line position columns
    color : str, optional
        Line color, by default "#9e9e9e"
    line_width : float, optional
        Line width in pixels, by default 1.5

    Returns
    -------
    tuple[go.Scatter, go.Scatter, go.Scatter]
        Tuple of three Scatter traces for month separator lines
    """
    line_style = {
        "mode": "lines",
        "line": {"color": color, "width": line_width},
        "hoverinfo": "skip",
    }

    # Vertical lines
    line1 = go.Scatter(
        x=df[["first_line_x", "first_line_x"]].values.flatten(),
        y=df[["first_line_y1", "first_line_y2"]].values.flatten(),
        **line_style,
    )

    # Horizontal lines
    line2 = go.Scatter(
        x=df[["second_line_x1", "second_line_x2"]].values.flatten(),
        y=df[["second_line_y", "second_line_y"]].values.flatten(),
        **line_style,
    )

    # Connecting vertical lines
    line3 = go.Scatter(
        x=df[["third_line_x", "third_line_x"]].values.flatten(),
        y=df[["third_line_y1", "third_line_y2"]].values.flatten(),
        **line_style,
    )

    return line1, line2, line3


def create_value_heatmap_trace(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    min_color: str = "#eeeeee",
    max_color: str = "#678fae",
    hover_template: str | None = None,
) -> go.Heatmap:
    """Create a heatmap trace for values.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with data
    date_col : str
        Name of date column
    value_col : str
        Name of value column
    min_color : str, optional
        Color for minimum values, by default "#eeeeee"
    max_color : str, optional
        Color for maximum values, by default "#678fae"
    hover_template : str | None, optional
        Custom hover template (None for default), by default None

    Returns
    -------
    go.Heatmap
        Heatmap trace for values
    """
    if hover_template is None:
        hover_template = "%{text}<br>Count: %{z}"

    return go.Heatmap(
        x=df["weeknum"],
        y=df["weekday"],
        z=df[value_col],
        xgap=3,
        ygap=3,
        text=df[date_col].dt.date,
        hovertemplate=hover_template,
        hoverlabel={"namelength": 0},
        colorscale=[
            [0.0, "#ffffff"],
            [0.0001, min_color],
            [1.0, max_color],
        ],
        showscale=False,
    )


def create_event_heatmap_trace(
    df: pd.DataFrame,
    event_col: str = "event",
    color: str = "#76cf61",
) -> go.Heatmap:
    """Create overlay heatmap trace for marking events.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with event column
    event_col : str, optional
        Name of event indicator column, by default "event"
    color : str, optional
        Color for event markers, by default "#76cf61"

    Returns
    -------
    go.Heatmap
        Heatmap trace for events
    """
    return go.Heatmap(
        x=df["weeknum"],
        y=df["weekday"],
        z=df[event_col],
        xgap=3,
        ygap=3,
        showscale=False,
        hoverinfo="skip",
        zmin=0,
        zmax=1,
        colorscale=[[0, "rgba(0,0,0,0)"], [1, color]],
    )


def add_event_markers(
    df: pd.DataFrame,
    event_dates: list[pd.Timestamp],
    date_col: str,
) -> pd.DataFrame:
    """Add event markers to DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with date information
    event_dates : list[pd.Timestamp]
        List of dates to mark as events
    date_col : str
        Name of date column

    Returns
    -------
    pd.DataFrame
        DataFrame with 'event' column added
    """
    result = df.copy()
    result["event"] = 0
    mask = result[date_col].isin(event_dates)
    result.loc[mask, "event"] = 1
    return result
