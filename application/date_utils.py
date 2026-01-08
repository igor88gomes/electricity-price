from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

STOCKHOLM_TZ = ZoneInfo("Europe/Stockholm")

MIN_DATE = date(2022, 11, 1)


def _today_stockholm() -> date:
    return datetime.now(STOCKHOLM_TZ).date()


def get_min_max_allowed_dates():
    min_date = MIN_DATE
    max_date = _today_stockholm() + timedelta(days=1)
    return min_date, max_date


def get_default_form_field_values():
    current_date = _today_stockholm()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    price_class = "SE3"
    return year, month, day, price_class


def is_valid_date(year, month, day):
    try:
        selected_date = date(year, month, day)
        min_date = MIN_DATE
        max_date = _today_stockholm() + timedelta(days=1)
        return min_date <= selected_date <= max_date
    except ValueError:
        return False


def validate_date(year, month, day):
    if not is_valid_date(year, month, day):
        return (
            "Sidan är begränsad till en dag i förväg och senast 2022-11-01 bakåt i tiden.",
            422,
        )
