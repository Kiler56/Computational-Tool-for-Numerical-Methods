"""
Gunicorn configuration for production deployment.
All values can be overridden via environment variables.
"""
import os
import multiprocessing

# ── Server socket ────────────────────────────────────────────
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:5000")

# ── Worker processes ─────────────────────────────────────────
workers = int(os.environ.get("GUNICORN_WORKERS", min(2 * multiprocessing.cpu_count() + 1, 4)))
threads = int(os.environ.get("GUNICORN_THREADS", 2))
worker_class = "gthread"

# ── Timeouts ─────────────────────────────────────────────────
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 120))
graceful_timeout = 30
keepalive = 5

# ── Application ──────────────────────────────────────────────
preload_app = True
wsgi_app = "run:app"

# ── Logging ──────────────────────────────────────────────────
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)sμs'

# ── Security ─────────────────────────────────────────────────
limit_request_line = 8190
limit_request_fields = 100
limit_request_field_size = 8190

# ── Process naming ───────────────────────────────────────────
proc_name = "numcalc"
