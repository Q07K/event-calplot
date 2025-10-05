"""Data preprocessing functions for calendar heatmap."""

import pandas as pd


def normalize_dates(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """Normalize datetime column to date only (no time component).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with data
    date_col : str
        Name of date column

    Returns
    -------
    pd.DataFrame
        DataFrame with normalized date column
    """
    result = df.copy()
    result[date_col] = pd.to_datetime(arg=result[date_col]).dt.normalize()
    return result


def create_full_date_range(start_year: int, end_year: int) -> pd.DataFrame:
    """Create a DataFrame with all dates in the year range.

    Parameters
    ----------
    start_year : int
        Start year (inclusive)
    end_year : int
        End year (inclusive)

    Returns
    -------
    pd.DataFrame
        DataFrame with a single column 'date' containing all dates in the range
    """
    return pd.DataFrame(
        data={
            "date": pd.date_range(
                start=f"{start_year}-01-01",
                end=f"{end_year}-12-31",
            )
        }
    )


def fill_missing_dates(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    years: list[int],
) -> pd.DataFrame:
    """Fill missing dates with zero values.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with data
    date_col : str
        Name of date column
    value_col : str
        Name of value column
    years : list[int]
        List of years to include

    Returns
    -------
    pd.DataFrame
        DataFrame with missing dates filled
    """
    start_year = min(years)
    end_year = max(years)

    date_df = create_full_date_range(start_year=start_year, end_year=end_year)
    date_df = date_df.rename(columns={"date": date_col})

    result = date_df.merge(right=df, how="outer")
    result[value_col] = result[value_col].fillna(value=0)

    return result


def add_weekday_info(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """Add weekday and week number information to DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with data
    date_col : str
        Name of date column

    Returns
    -------
    pd.DataFrame
        DataFrame with added weekday and week number information
    """
    result = df.copy()

    # Weekday (0=Monday, 6=Sunday)
    result["weekday"] = result[date_col].dt.weekday

    # Week number (ISO week, 1-53)
    result["weeknum"] = (
        result[date_col].dt.strftime(date_format="%V").astype(dtype=int)
    )

    # Adjust week numbers for edge cases
    # January dates that belong to previous year's last week
    jan_mask = (result[date_col].dt.month == 1) & (result["weeknum"] >= 52)
    result.loc[jan_mask, "weeknum"] = 0

    # December dates that belong to next year's first week
    dec_mask = (result[date_col].dt.month == 12) & (result["weeknum"] == 1)
    result.loc[dec_mask, "weeknum"] = 53

    return result


def preprocess_data(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
) -> pd.DataFrame:
    """Preprocess calendar heatmap data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with data
    date_col : str
        Name of date column
    value_col : str
        Name of value column

    Returns
    -------
    pd.DataFrame
        DataFrame with preprocessed calendar heatmap data
    """

    # Normalize dates
    result = normalize_dates(df=df, date_col=date_col)

    # Get year range
    years = result[date_col].dt.year.unique().tolist()

    # Fill missing dates
    result = fill_missing_dates(
        df=result,
        date_col=date_col,
        value_col=value_col,
        years=years,
    )

    # Add weekday information
    result = add_weekday_info(df=result, date_col=date_col)

    return result


def get_years_in_data(df: pd.DataFrame, date_col: str) -> list[int]:
    """Extract unique years from date column.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with data
    date_col : str
        Name of date column

    Returns
    -------
    list[int]
        List of unique years present in the date column
    """
    return sorted(df[date_col].dt.year.unique().tolist())


def filter_by_year(df: pd.DataFrame, date_col: str, year: int) -> pd.DataFrame:
    """Filter DataFrame to only include data from specified year.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with data
    date_col : str
        Name of date column
    year : int
        Year to filter by

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame
    """
    return df[df[date_col].dt.year == year].copy()
