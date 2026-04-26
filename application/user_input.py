from flask import request

ALLOWED_PRICE_CLASSES = {"SE1", "SE2", "SE3", "SE4"}


def get_user_input():
    try:
        year = int(request.form.get("year", ""))
        month = int(request.form.get("month", ""))
        day = int(request.form.get("day", ""))
    except ValueError as exc:
        raise ValueError("Invalid date input.") from exc

    price_class = request.form.get("price_class", "")

    if price_class not in ALLOWED_PRICE_CLASSES:
        raise ValueError("Invalid price area.")

    return year, month, day, price_class
