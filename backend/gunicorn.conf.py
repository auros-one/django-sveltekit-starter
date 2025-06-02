"""gunicorn configuration."""

import multiprocessing
import os

try:  # pragma: no cover
    from rich import traceback

    traceback.install(show_locals=True)
except ImportError:  # pragma: no cover
    pass

accesslog = "-"
bind = [f"0.0.0.0:{os.environ.get('PORT', 8000)}"]
max_requests = 1000
max_requests_jitter = 50
reload = os.environ.get("GUNICORN_RELOAD") == "1"
timeout = 0
workers = os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1)
wsgi_app = "project.wsgi"
