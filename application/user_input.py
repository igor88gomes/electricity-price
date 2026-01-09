from flask import request

ALLOWED_PRICE_CLASSES = {"SE1", "SE2", "SE3", "SE4"}


def get_user_input():
    year = int(request.form["year"])
    month = int(request.form["month"])
    day = int(request.form["day"])
    price_class = request.form["price_class"]

    if price_class not in ALLOWED_PRICE_CLASSES:
        raise ValueError("Ogiltig prisklass.")

    return year, month, day, price_class
