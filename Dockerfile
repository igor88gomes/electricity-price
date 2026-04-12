# Base image pinned by manifest digest for reproducible builds and controlled security updates
FROM python:3.12.13-alpine3.22@sha256:f6973b8f9395204414a7f25d99a50ba1c7306064771d11a8c2a848e9af3697a6

# Avoid .pyc files and enable unbuffered stdout logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Update Alpine packages before installing Python dependencies
RUN apk update && apk upgrade --no-cache

# Create a non-root user with a fixed UID for better runtime security
RUN adduser --disabled-password --gecos "" --uid 1000 appuser

WORKDIR /app

# Install runtime dependencies only
COPY requirements.txt .

RUN python -m pip install --upgrade "pip>=26,<27" --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser application ./application

# Gunicorn runtime settings for predictable performance
ENV GUNICORN_CMD_ARGS="--workers=2 --threads=2 --timeout=60 --graceful-timeout=30"

EXPOSE 8000

USER appuser

# Health check against /healthz
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz').getcode()==200 else 1)"

# Gunicorn target: <module>:<Flask app>
CMD ["gunicorn", "-b", "0.0.0.0:8000", "application.app:app"]