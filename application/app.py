# --- Nya imports för mätning/observabilitet ---
import time

from flask import Flask, Response, g, render_template, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from application.date_utils import (
    get_default_form_field_values,
    get_min_max_allowed_dates,
    validate_date,
)
from application.electricity_price_data import fetch_and_process_elpris_data
from application.electricity_price_visualization import create_chart, create_pandas_table
from application.menu_options import menu_options
from application.user_input import get_user_input

app = Flask(__name__)

# --------------------------------------------------------------------
# Metrik för HTTP-trafik (Prometheus)
# --------------------------------------------------------------------
# Räkna antal HTTP-anrop per metod/endpoint/status
HTTP_REQUESTS = Counter("app_http_requests_total", "Totalt antal HTTP-anrop", ["method", "endpoint", "http_status"])

# Mäta latens per endpoint (i sekunder)
HTTP_LATENCY = Histogram("app_request_latency_seconds", "Latens för HTTP-anrop (sekunder)", ["endpoint"])


# Före varje request: starta en timer
@app.before_request
def _metrics_start_timer():
    g._start_time = time.time()


# Efter varje request: registrera latens och öka räknare
@app.after_request
def _metrics_record(response):
    try:
        elapsed = time.time() - getattr(g, "_start_time", time.time())
        endpoint = request.endpoint or "unknown"
        HTTP_LATENCY.labels(endpoint=endpoint).observe(elapsed)
        HTTP_REQUESTS.labels(method=request.method, endpoint=endpoint, http_status=response.status_code).inc()
    except Exception:
        # Metrik får aldrig krascha applikationen
        pass
    return response


# --------------------------------------------------------------------
# Hälsosidor (liveness/readiness) och metrics-endpoint
# --------------------------------------------------------------------
@app.get("/healthz")
def healthz():
    """
    Liveness-kontroll.

    Returnerar 200 om processen lever (används som livenessProbe).
    """
    return "ok", 200


@app.get("/readyz")
def readyz():
    """
    Readiness-kontroll.

    Returnerar 200 om applikationen är redo att ta emot trafik.
    (Här kan man vid behov lägga in en lätt kontroll av beroenden.)
    """
    return "ready", 200


@app.get("/metrics")
def metrics():
    """
    Prometheus-metrik.

    Exponerar standard- och applikationsmetrik i Prometheus-format.
    """
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


# Route till startsidan
@app.route("/")
def index():
    """
    Rendera startsidan.

    Denna funktion hanterar begäranden till rot-URL:en ('/')
    och renderar index.html-mallen med data.

    Returns:
        Renderad HTML-mall
    """
    # Hämta minsta och största tillåtna datum
    min_date, next_day = get_min_max_allowed_dates()

    # Hämta standardvärden för år, månad, dag och prisgrupp i formuläret
    year, month, day, price_class = get_default_form_field_values()

    # Rendera index.html-mallen med data
    return render_template(
        "index.html",
        year=year,
        month=month,
        day=day,
        price_class=price_class,
        menu_options=menu_options,
        min_date=min_date,
        next_day=next_day,
    )


@app.route("/calculate", methods=["POST"])
def calculate_prices():
    """
    Beräkna elpriser.

    Denna funktion hanterar POST-begäranden till URL:en
    '/calculate' och utför beräkningar baserade på
    användarinput.

    Returns:
        Renderad HTML-mall med beräknad data
    """
    # Hämta användarinput från formuläret
    year, month, day, price_class = get_user_input()

    # Validera användarinput
    validation_error = validate_date(year, month, day)

    if validation_error:
        # Returnera ett valideringsfel svar
        return validation_error

    # Hämta och behandla elprisdata med den importerade funktionen
    current_prices, date = fetch_and_process_elpris_data(year, month, day, price_class)

    # Hantera fallet när current_prices är None
    if current_prices is None:
        return (
            "Åtkomst till nästa dags elprisdata kommer att vara tillgänglig efter kl. 13:00.",
            200,
        )

    pandas_table = create_pandas_table(current_prices)
    chart_html = create_chart(current_prices, date, price_class)

    # Rendera result.html-mallen med data
    return render_template(
        "result.html",
        date=date,
        price_class=price_class,
        current_prices=current_prices,
        error_message=None,
        pandas_table=pandas_table,
        chart_html=chart_html,
    )


# Felhanterare för 404 Not Found-fel
@app.errorhandler(404)
def handle_not_found_error(error):
    """
    Hantera 404 Not Found-fel.

    Denna funktion hanterar 404-fel genom att returnera ett
    anpassat felmeddelande.

    Returns:
        Felmeddelande och HTTP-statuskoden 404
    """
    return "Sidan hittades inte.", 404


# Route för att utlösa ett internt fel
@app.route("/trigger_internal_error", methods=["GET"])
def trigger_internal_error():
    """
    Utlösa ett internt fel.

    Denna funktion höjer ett undantag för att utlösa
    ett internt fel.

    Returns:
        Höjer ett undantag (500 Internal Server Error)
    """
    raise Exception("Detta är ett internt fel")


# Felhanterare för 500 Internal Server Error
@app.errorhandler(500)
def handle_internal_server_error(error):
    """
    Hantera 500 Internal Server Error.

    Denna funktion hanterar 500-fel genom att returnera ett
    anpassat felmeddelande.

    Returns:
        Felmeddelande och HTTP-statuskoden 500
    """
    return "Intern Serverfel: " + str(error), 500


if __name__ == "__main__":
    app.run(debug=True)
