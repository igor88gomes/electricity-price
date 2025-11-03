import re

import pytest

from application.app import app


@pytest.fixture
def client():
    """
    Skapar en testklient för Flask-applikationen.
    Används av varje test för att göra HTTP-anrop utan att starta en riktig server.
    """
    return app.test_client()


def test_healthz_ok(client):
    """
    Verifierar liveness-endpointen (/healthz).
    Förväntat: HTTP 200 och texten 'ok'.
    """
    r = client.get("/healthz")
    assert r.status_code == 200
    assert b"ok" in r.data


def test_readyz_ok(client):
    """
    Verifierar readiness-endpointen (/readyz).
    Förväntat: HTTP 200 och texten 'ready'.
    """
    r = client.get("/readyz")
    assert r.status_code == 200
    assert b"ready" in r.data


def test_metrics_exposes_custom_metrics(client):
    """
    Säkerställer att Prometheus-metrik exponeras på /metrics
    och att våra egna metriknamn finns med.

    Steg:
      1) Gör en vanlig request (/) så att räknare/latens uppdateras.
      2) Hämta /metrics och kontrollera att metriknamnen finns.
      3) (Valfritt) Kontrollera att värdet är >= 1.
    """
    # 1) Generera minst ett anrop så att metrik uppdateras
    r_home = client.get("/")
    assert r_home.status_code in (200, 301, 302) or r_home.status_code == 200

    # 2) Hämta /metrics
    r = client.get("/metrics")
    assert r.status_code == 200
    text = r.data.decode("utf-8")

    # 2a) Kontrollera att våra metriknamn förekommer i output
    assert "app_http_requests_total" in text
    assert "app_request_latency_seconds" in text

    # 3) Validera att räknaren har åtminstone ett värde
    m = re.search(r"app_http_requests_total\{.*\}\s+(\d+(\.\d+)?)", text)
    assert m is not None
