from flask import request


def get_user_input():
    year = int(request.form["year"])
    month = int(request.form["month"])
    day = int(request.form["day"])
    price_class = request.form["price_class"]
    return year, month, day, price_class
