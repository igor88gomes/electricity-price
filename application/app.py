import logging
import time

from flask import Flask, Response, g, render_template, request, url_for
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from application.date_utils import get_default_form_field_values, get_min_max_allowed_dates, validate_date
from application.electricity_price_data import fetch_and_process_elpris_data
from application.electricity_price_visualization import create_chart, create_pandas_table
from application.menu_options import menu_options
from application.user_input import get_user_input

logger = logging.getLogger(__name__)

app = Flask(__name__)

HTTP_REQUESTS = Counter(
    "app_http_requests_total",
    "Totalt antal HTTP-anrop",
    ["method", "endpoint", "http_status"],
)
HTTP_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Latens för HTTP-anrop (sekunder)",
    ["endpoint"],
)


@app.before_request
def _metrics_start_timer():
    g._start_time = time.perf_counter()


@app.after_request
def _metrics_record(response):
    try:
        elapsed = time.perf_counter() - getattr(g, "_start_time", time.perf_counter())
        endpoint = request.endpoint or "unknown"
        HTTP_LATENCY.labels(endpoint=endpoint).observe(elapsed)
        HTTP_REQUESTS.labels(method=request.method, endpoint=endpoint, http_status=response.status_code).inc()
    except Exception:
        logger.exception("Failed to record metrics")
    return response


@app.get("/healthz")
def healthz():
    return "ok", 200


@app.get("/readyz")
def readyz():
    return "ready", 200


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.get("/")
def index():
    min_date, next_day = get_min_max_allowed_dates()
    year, month, day, price_class = get_default_form_field_values()
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


@app.post("/calculate")
def calculate_prices():
    year, month, day, price_class = get_user_input()

    validation_error = validate_date(year, month, day)
    if validation_error:
        message, status = validation_error
        return (
            render_template(
                "message.html",
                title="Ogiltigt datum",
                message=message,
                severity="danger",
                back_url=url_for("index"),
            ),
            status,
        )

    current_prices, date, err = fetch_and_process_elpris_data(
        year,
        month,
        day,
        price_class,
    )

    if err == "no_data":
        return (
            render_template(
                "message.html",
                title="Elprisdata ej tillgänglig ännu",
                message="Åtkomst till nästa dags elprisdata kommer att vara tillgänglig efter kl. 13:00.",
                severity="warning",
                back_url=url_for("index"),
            ),
            503,
        )

    return render_template(
        "result.html",
        date=date,
        price_class=price_class,
        current_prices=current_prices,
        error_message=None,
        pandas_table=create_pandas_table(current_prices),
        chart_html=create_chart(current_prices, date, price_class),
    )


@app.errorhandler(404)
def handle_not_found_error(_error):
    return (
        render_template(
            "message.html",
            title="Sidan hittades inte",
            message="Sidan du försökte nå finns inte.",
            severity="warning",
            back_url=url_for("index"),
        ),
        404,
    )


@app.errorhandler(500)
def handle_internal_server_error(error):
    details = str(error) if app.debug else None
    return (
        render_template(
            "message.html",
            title="Intern Serverfel",
            message="Ett oväntat fel inträffade. Försök igen senare.",
            details=details,
            severity="danger",
            back_url=url_for("index"),
        ),
        500,
    )


if __name__ == "__main__":
    app.run()
