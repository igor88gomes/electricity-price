from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from application.date_utils import (
    get_default_form_field_values,
    get_min_max_allowed_dates,
    is_valid_date,
    validate_date,
)

STOCKHOLM_TZ = ZoneInfo("Europe/Stockholm")


def test_get_min_max_allowed_dates():
    min_date, max_date = get_min_max_allowed_dates()

    assert min_date == date(2022, 11, 1)

    today_stockholm = datetime.now(STOCKHOLM_TZ).date()
    assert max_date == today_stockholm + timedelta(days=1)


def test_get_default_form_field_values():
    year, month, day, price_class = get_default_form_field_values()

    assert isinstance(year, int)
    assert isinstance(month, int)
    assert isinstance(day, int)
    assert price_class == "SE3"


def test_is_valid_date():
    assert is_valid_date(2022, 11, 1) is True
    assert is_valid_date(2022, 10, 31) is False


def test_validate_date():
    assert validate_date(2022, 11, 1) is None

    error_message, status_code = validate_date(2022, 10, 31)
    assert status_code == 422
    assert error_message == "Sidan är begränsad till en dag i förväg och senast 2022-11-01 bakåt i tiden."
