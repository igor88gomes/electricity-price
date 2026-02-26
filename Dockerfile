# Basimage låst med manifest-digest för reproducerbara builds och kontrollerade säkerhetsuppdateringar
FROM python:3.12-slim@sha256:39e4e1ccb01578e3c86f7a0cf7b7fd89b8dbe2c27a88de11cf726ba669469f49

# Miljövariabler för att undvika .pyc-filer och få omedelbar loggning i stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Skapa en icke-root användare med fast UID (1000) för bättre säkerhet
RUN adduser --disabled-password --gecos "" --uid 1000 appuser

WORKDIR /app

# Beroenden för ren runtime-image (hålls separerade från testberoenden)
COPY requirements.txt .

RUN python -m pip install --upgrade "pip>=26,<27" --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser application ./application

# Driftinställningar för Gunicorn (workers/threads + timeouts) för förutsägbar prestanda
ENV GUNICORN_CMD_ARGS="--workers=2 --threads=2 --timeout=60 --graceful-timeout=30"

EXPOSE 8000

USER appuser

# Hälsokontroll mot /healthz
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz').getcode()==200 else 1)"

# gunicorn target: <modul>:<Flask-app>
CMD ["gunicorn", "-b", "0.0.0.0:8000", "application.app:app"]
