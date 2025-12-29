import pytest
from flask import Flask

from application.user_input import get_user_input


@pytest.mark.parametrize(
    "form, expected",
    [
        ({"year": "2023", "month": "11", "day": "10", "price_class": "SE1"}, (2023, 11, 10, "SE1")),
        ({"year": "2022", "month": "10", "day": "10", "price_class": "SE4"}, (2022, 10, 10, "SE4")),
    ],
)
def test_get_user_input(form, expected):
    app = Flask(__name__)

    with app.test_request_context(method="POST", data=form):
        assert get_user_input() == expected
