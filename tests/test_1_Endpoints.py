from datetime import datetime, timedelta

import pytest

from application.app import app


# Definiera en testklient för Flask-appen
@pytest.fixture
def client():
    return app.test_client()


# Test för att kontrollera om startsidan (GET) svarar med statuskoden 200
def test_home_page_method_get(client):
    response = client.get("/")
    assert response.status_code == 200


# Test för att kontrollera att startsidan (POST) returnerar statuskoden 405 (Metod ej tillåten)
def test_home_page_method_post(client):
    response = client.post("/")
    assert response.status_code == 405


# Testa beräkning av elpris med parametrar nära gränsen för giltiga datum
def test_invalid_date_calculation(client):
    response = client.post("/calculate", data=dict(year="2022", month="10", day="31", price_class="SE1"))
    assert response.status_code == 404


# Testa beräkning av elpris för första giltiga dagen
def test_first_valid_date_calculation(client):
    response = client.post("/calculate", data=dict(year="2022", month="11", day="1", price_class="SE4"))
    assert response.status_code == 200
    assert b"Elprisresultat" in response.data


# Testa kl 13.00. Fram till kl. 13.00 finns en begränsning för publicering av följande dags uppgifter
def test_13_o_clock_page(client):
    current_date = datetime.now()

    if current_date.hour < 13:
        expected_date = current_date.replace(hour=13, minute=0, second=0, microsecond=0)
    else:
        expected_date = (current_date + timedelta(days=1)).replace(hour=13, minute=0, second=0, microsecond=0)

    year, month, day = expected_date.year, expected_date.month, expected_date.day

    response = client.post("/calculate", data={"year": year, "month": month, "day": day, "price_class": "SE3"})
    assert response.status_code == 200


# Testa en ogiltig URL (inte befintlig endpoint)
def test_invalid_endpoint(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404


# Testa intern serverfel genom att utlösa ett undantag i appen
def test_internal_server_error(client):
    response = client.get("/trigger_internal_error")
    assert response.status_code == 500
    assert b"Intern Serverfel" in response.data


if __name__ == "__main__":
    pytest.main()
