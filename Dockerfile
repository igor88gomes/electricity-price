FROM python:3.12-slim

# Miljövariabler för att undvika .pyc-filer och få omedelbar loggning i stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Skapa en icke-root användare med fast UID (1000) för bättre säkerhet
RUN adduser --disabled-password --gecos "" --uid 1000 appuser

# Arbetskatalog inne i containern
WORKDIR /app

# Kopiera Python-beroenden
COPY requirements.txt .

# Uppdatera pip till en säker version och installera beroenden
RUN python -m pip install --upgrade "pip>=25.3" --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Kopiera applikationskoden (inkl. templates/static) till containern
# Strukturen förväntas vara: /app/application/...
COPY application ./application

# Säkerställ att appuser äger katalogen /app
RUN chown -R appuser:appuser /app

# Standardport och Gunicorn-flaggar (enkla värden för demo/prod-lik miljö)
ENV PORT=8000 \
    GUNICORN_CMD_ARGS="--workers=2 --threads=2 --timeout=60"

# Exponera porten där appen lyssnar
EXPOSE 8000

# Kör som icke-root användare
USER appuser

# Hälsokontroll: kollar /healthz var 30:e sekund (behöver att appen redan kör)
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz').getcode()==200 else 1)"

# Startkommando: Gunicorn som WSGI-server, binder på alla interface
# 'application.app:app' = <paket/modul>:<Flask-app-objekt>
CMD ["gunicorn", "-b", "0.0.0.0:8000", "application.app:app"]
