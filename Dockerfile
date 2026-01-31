FROM python:3.12-slim

# Miljövariabler för att undvika .pyc-filer och få omedelbar loggning i stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Uppdaterar systempaket i basimagen som en del av grundläggande säkerhets- och underhållspraxis
RUN apt-get update \
 && apt-get upgrade -y \
 && rm -rf /var/lib/apt/lists/*

# Skapa en icke-root användare med fast UID (1000) för bättre säkerhet
RUN adduser --disabled-password --gecos "" --uid 1000 appuser

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade "pip>=25.3" --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

COPY application ./application

RUN chown -R appuser:appuser /app

ENV GUNICORN_CMD_ARGS="--workers=2 --threads=2 --timeout=60 --graceful-timeout=30"

EXPOSE 8000

USER appuser

# Hälsokontroll mot /healthz
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz').getcode()==200 else 1)"

# gunicorn target: <modul>:<Flask-app>
CMD ["gunicorn", "-b", "0.0.0.0:8000", "application.app:app"]
