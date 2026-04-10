# Basimage låst med manifest-digest för reproducerbara builds och kontrollerade säkerhetsuppdateringar
FROM python:3.12.13-slim-trixie@sha256:804ddf3251a60bbf9c92e73b7566c40428d54d0e79d3428194edf40da6521286

# Miljövariabler för att undvika .pyc-filer och få omedelbar loggning i stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Skapa en icke-root användare med fast UID (1000) för bättre säkerhet
RUN adduser --disabled-password --gecos "" --uid 1000 appuser

WORKDIR /app

# Endast runtime-beroenden installeras i image; testberoenden hålls utanför runtime-builden
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
