# ═══════════════════════════════════════════════════════════════
# Stage 1: Builder — install dependencies in a temporary image
# ═══════════════════════════════════════════════════════════════
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build-time system deps (numpy needs them)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ═══════════════════════════════════════════════════════════════
# Stage 2: Runtime — lean production image
# ═══════════════════════════════════════════════════════════════
FROM python:3.11-slim AS runtime

# OCI image labels
LABEL org.opencontainers.image.title="Numerical Methods Calculator" \
      org.opencontainers.image.description="Flask web app for numerical methods" \
      org.opencontainers.image.source="https://github.com/" \
      org.opencontainers.image.vendor="NumCalc"

# Create non-root user
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app/ ./app/
COPY run.py gunicorn.conf.py ./

# Create instance directory for SQLite and set permissions
RUN mkdir -p /app/instance && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose internal port (Nginx will proxy to this)
EXPOSE 5000

# Healthcheck: verify the app is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1

# Start with Gunicorn using config file
CMD ["gunicorn", "--config", "gunicorn.conf.py"]
