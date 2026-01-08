import re

import pytest

from application.app import app


@pytest.fixture
def client():
    return app.test_client()


def test_healthz_ok(client, get_text):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert get_text(r) == "ok"


def test_readyz_ok(client, get_text, monkeypatch):
    class _Conn:
        def __enter__(self): return self
        def __exit__(self, exc_type, exc, tb): return False

    monkeypatch.setattr("application.app.socket.create_connection", lambda *_a, **_kw: _Conn())

    r = client.get("/readyz")
    assert r.status_code == 200
    assert get_text(r) == "ready"


def test_metrics_exposes_custom_metrics(client, get_text):
    assert client.get("/").status_code == 200

    r = client.get("/metrics")
    assert r.status_code == 200

    text = get_text(r)
    assert "app_http_requests_total" in text
    assert "app_request_latency_seconds" in text

    m = re.search(r"app_http_requests_total\{.*\}\s+(\d+(\.\d+)?)", text)
    assert m is not None


def test_metrics_latency_has_healthz_label(client, get_text):
    client.get("/healthz")

    r = client.get("/metrics")
    assert r.status_code == 200
    text = get_text(r)

    assert (
        re.search(
            r'app_request_latency_seconds_(count|sum)\{endpoint="healthz"\}',
            text,
        )
        is not None
    )
