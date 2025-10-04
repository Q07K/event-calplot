"""Locale support for date labels in different languages."""

from typing import TypedDict


class DateLabels(TypedDict):
    """A TypedDict for date labels in different languages."""

    months: list[str]
    weekdays: list[str]


LOCALES: dict[str, DateLabels] = {
    "en": {
        "months": [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        "weekdays": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "ko": {
        "months": [
            "1월",
            "2월",
            "3월",
            "4월",
            "5월",
            "6월",
            "7월",
            "8월",
            "9월",
            "10월",
            "11월",
            "12월",
        ],
        "weekdays": ["월", "화", "수", "목", "금", "토", "일"],
    },
    # Add more languages as needed
}


def get_locale_text(language: str = "en") -> DateLabels:
    """Get date labels for a specific language.

    The weekdays start from Monday.

    Supported languages:
    - "en": English
    - "ko": Korean


    Parameters
    ----------
    language : str, optional
        The language code for the desired locale, by default "en"

    Returns
    -------
    DateLabels
        The date labels for the specified language

    Raises
    ------
    ValueError
        If the specified language is not supported
    """

    locale = LOCALES.get(language)
    if locale is None:
        raise ValueError(
            f"Unsupported language code '{language}'."
            f"Supported languages are: {', '.join(LOCALES.keys())}."
        )
    return locale
