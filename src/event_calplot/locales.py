"""Locale support for date labels in different languages."""

from typing import TypedDict


class DateLabels(TypedDict):
    """A TypedDict for date labels in different languages."""

    months: list[str]
    weekdays: list[str]


def get_locale_text(language: str = "en") -> DateLabels:
    """Get date labels for a specific language.

    Supported languages:
    - "en": English
    - "ko": Korean

    The weekdays start from Monday.

    Parameters
    ----------
    language : str, optional
        The language code for the desired locale, by default "en"

    Returns
    -------
    DateLabels
        The date labels for the specified language
    """

    locales: dict[str, DateLabels] = {
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
    locale = locales.get(language)
    if locale is None:
        raise ValueError(
            f"Unsupported language code '{language}'. Supported languages are: {', '.join(locales.keys())}."
        )
    return locale
