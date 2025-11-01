from flask import Flask
from application.user_input import get_user_input


# Kontrollera att get_user_input() returnerar rätt värden beroende på inmatad data
def test_get_user_input():
    # Flask-app för att använda test_request_context
    app = Flask(__name__)

    # Kontrollera inmatning för år 2023, månad 11, dag 10 och prisklass 'SE1'
    with app.test_request_context(method='POST', data={'year': '2023', 'month': '11', 'day': '10', 'price_class': 'SE1'}):
        year, month, day, price_class = get_user_input()
        assert year == 2023
        assert month == 11
        assert day == 10
        assert price_class == 'SE1'

        # Kontrollera inmatning för år 2023, månad 11, dag 10 och prisklass 'SE4'
        with app.test_request_context(method='POST',
                                      data={'year': '2022', 'month': '10', 'day': '10', 'price_class': 'SE4'}):
            year, month, day, price_class = get_user_input()
            assert year == 2022
            assert month == 10
            assert day == 10
            assert price_class == 'SE4'




