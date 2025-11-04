from datetime import datetime, timedelta

from application.date_utils import (
    get_default_form_field_values,
    get_min_max_allowed_dates,
    is_valid_date,
    validate_date,
)


# Testa get_min_max_allowed_dates funktionen
def test_get_min_max_allowed_dates():
    min_date, max_date = get_min_max_allowed_dates()
    assert min_date == datetime(2022, 11, 1)
    assert max_date.date() == (datetime.now() + timedelta(days=1)).date()


# Testa get_default_form_field_values funktionen
def test_get_default_form_field_values():
    year, month, day, price_class = get_default_form_field_values()
    assert isinstance(year, int)
    assert isinstance(month, int)
    assert isinstance(day, int)
    assert isinstance(price_class, str)


# Testa is_valid_date funktionen
def test_is_valid_date():
    assert is_valid_date(2022, 11, 1)
    assert not is_valid_date(2022, 10, 31)


# Testa validate_date funktionen
def test_validate_date():
    assert validate_date(2022, 11, 1) is None
    error_message, status_code = validate_date(2022, 10, 31)
    assert error_message == "Sidan är begränsad till en dag i förväg och senast 2022-11-01 bakåt i tiden."
    assert status_code == 404
