import pytest
import requests
from application.electricity_price_data import extract_date_from_elpris_data, get_elpris_data_from_api


# Mocka requests-modulen för att testa get_elpris_data_from_api
@pytest.fixture
def mock_requests_get(monkeypatch):
    class MockResponse:
        @staticmethod
        def raise_for_status():
            pass

        def json(self):
            return [{"time_start": "2023-11-05T00:00:00Z"}]  # Exempeldata

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


# Testa extract_date_from_elpris_data funktionen
def test_extract_date_from_elpris_data():
    data = [{"time_start": "2023-11-05T00:00:00Z"}]
    date = extract_date_from_elpris_data(data)
    assert date == "2023-11-05"


# Testa get_elpris_data_from_api funktionen
def test_get_elpris_data_from_api(mock_requests_get):
    api_url = "https://elprisetjustnu.com/api/data.json"
    data = get_elpris_data_from_api(api_url)
    assert data == [{"time_start": "2023-11-05T00:00:00Z"}]
