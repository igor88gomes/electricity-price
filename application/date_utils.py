from datetime import datetime, timedelta


def get_min_max_allowed_dates():
    min_date = datetime(2022, 11, 1)
    max_date = datetime.now() + timedelta(days=1)
    return min_date, max_date


def get_default_form_field_values():
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    price_class = "SE3"
    return year, month, day, price_class


def is_valid_date(year, month, day):
    try:
        date = datetime(year, month, day)
        min_date = datetime(2022, 11, 1)
        max_date = datetime.now() + timedelta(days=1)
        return min_date <= date <= max_date
    except ValueError:
        return False


def validate_date(year, month, day):
    if not is_valid_date(year, month, day):
        return "Sidan är begränsad till en dag i förväg och senast 2022-11-01 bakåt i tiden.", 422
