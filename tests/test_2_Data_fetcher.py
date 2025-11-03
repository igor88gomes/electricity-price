import requests

from application.data_fetcher import get_elpris_data_from_api


# Definiera klassen MockResponse
class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(f"Statuskod: {self.status_code}")


# Testa en lyckad begäran (statuskod 200)
def test_get_elpris_data_from_api_success(monkeypatch):
    def mock_requests_get(api_url):
        return MockResponse(200, {"key": "value"})

    monkeypatch.setattr(requests, "get", mock_requests_get)

    api_url = "https://elprisetjustnu.com/api/data"
    response = get_elpris_data_from_api(api_url)

    assert response is not None
    assert response["key"] == "value"


# Testa en misslyckad begäran (statuskod 404)
def test_fetch_elpris_data_failure(monkeypatch):
    def mock_requests_get(api_url):
        return MockResponse(404, {"error": "Not Found"})

    monkeypatch.setattr(requests, "get", mock_requests_get)

    api_url = "https://elprisetjustnu.com/api/data"
    response = get_elpris_data_from_api(api_url)

    assert response is None
