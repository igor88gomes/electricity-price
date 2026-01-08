import requests

from application.data_fetcher import get_elpris_data_from_api


def test_get_elpris_data_from_api_success(monkeypatch):
    class _Response:
        def raise_for_status(self):
            return None

        def json(self):
            return {"key": "value"}

    monkeypatch.setattr(requests, "get", lambda _url, **_kwargs: _Response())

    response = get_elpris_data_from_api("https://example.test/api/data")
    assert response == {"key": "value"}


def test_get_elpris_data_from_api_failure(monkeypatch):
    class _Response:
        def raise_for_status(self):
            raise requests.exceptions.HTTPError("Statuskod: 404")

        def json(self):
            return {"error": "Not Found"}

    monkeypatch.setattr(requests, "get", lambda _url, **_kwargs: _Response())

    response = get_elpris_data_from_api("https://example.test/api/data")
    assert response is None


def test_get_elpris_data_from_api_request_exception(monkeypatch):
    monkeypatch.setattr(
        requests,
        "get",
        lambda _url, **_kwargs: (_ for _ in ()).throw(requests.exceptions.RequestException()),
    )

    response = get_elpris_data_from_api("https://example.test/api/data")
    assert response is None
