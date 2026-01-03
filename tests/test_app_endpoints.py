import pandas as pd
import pytest

from application.app import app, handle_internal_server_error


@pytest.fixture
def client():
    return app.test_client()


def test_home_page_method_get(client, get_text):
    response = client.get("/")
    assert response.status_code == 200
    assert "Electricity Price" in get_text(response)


def test_home_page_method_post(client, get_text):
    response = client.post("/")
    assert response.status_code == 405
    assert "Method Not Allowed" in get_text(response)


def test_invalid_date_calculation(client, get_text):
    response = client.post(
        "/calculate",
        data={"year": "2022", "month": "10", "day": "31", "price_class": "SE1"},
    )
    assert response.status_code == 422
    assert "Ogiltigt datum" in get_text(response)


def test_calculate_success_renders_result(client, monkeypatch, get_text):
    def _fake_fetch_and_process_elpris_data(year, month, day, price_class):
        df = pd.DataFrame(
            {
                "Tidpunkt på dygnet i (hh:mm)": ["00:00", "01:00"],
                "Motsvarande pris i (kr/kWh)": [0.1, 0.2],
            }
        )
        return df, "2022-11-01", None

    monkeypatch.setattr(
        "application.app.fetch_and_process_elpris_data",
        _fake_fetch_and_process_elpris_data,
    )

    response = client.post(
        "/calculate",
        data={"year": "2022", "month": "11", "day": "1", "price_class": "SE3"},
    )

    assert response.status_code == 200
    assert "Elprisresultat" in get_text(response)


def test_calculate_returns_no_data_message(client, monkeypatch, get_text):
    def _fake_fetch_and_process_elpris_data(year, month, day, price_class):
        return None, None, "no_data"

    monkeypatch.setattr(
        "application.app.fetch_and_process_elpris_data",
        _fake_fetch_and_process_elpris_data,
    )

    response = client.post(
        "/calculate",
        data={"year": "2022", "month": "11", "day": "1", "price_class": "SE3"},
    )

    assert response.status_code == 503
    text = get_text(response)
    assert "efter kl. 13:00" in text
    assert "Elprisdata ej tillgänglig ännu" in text


def test_invalid_endpoint(client, get_text):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert "Sidan hittades inte" in get_text(response) or "Sidan du försökte nå finns inte" in get_text(response)


def test_404_handler_returns_message(client, get_text):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert "Sidan du försökte nå finns inte." in get_text(response)

@pytest.mark.skip(reason="temporary skip to test coverage badge")
def test_internal_server_error(client):
    with app.test_request_context("/"):
        response, status = handle_internal_server_error(RuntimeError("boom"))

    assert status == 500
    assert "Intern Serverfel" in response
