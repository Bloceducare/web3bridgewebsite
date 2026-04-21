"""
Gunicorn process model for production (Koyeb, VM, etc.).

Start from the ``backend_v2`` directory (same as ``manage.py``):

    gunicorn backend_v2.wsgi:application -c gunicorn.conf.py

Environment overrides:
  PORT / WEB_PORT           Bind port (Koyeb sets PORT).
  GUNICORN_WORKERS          Process count (default: min(2*CPU+1, 4)).
  WEB_CONCURRENCY           Alias for GUNICORN_WORKERS (common on PaaS).
  GUNICORN_THREADS          Per-worker threads when using gthread (default 4).
  GUNICORN_WORKER_CLASS     Default ``gthread`` (I/O-bound APIs); use ``sync`` if preferred.
  GUNICORN_TIMEOUT          Worker silent timeout in seconds (default 120).
  GUNICORN_GRACEFUL_TIMEOUT Seconds to finish requests after SIGTERM (default 30).
  GUNICORN_MAX_REQUESTS     Restart workers after N requests (default 2000); jitter optional.
"""
import multiprocessing
import os

bind = f"0.0.0.0:{os.environ.get('PORT', os.environ.get('WEB_PORT', '8000'))}"

_workers_raw = os.environ.get("GUNICORN_WORKERS") or os.environ.get("WEB_CONCURRENCY")
if _workers_raw:
    workers = max(1, int(_workers_raw))
else:
    workers = min(multiprocessing.cpu_count() * 2 + 1, 4)

worker_class = os.environ.get("GUNICORN_WORKER_CLASS", "gthread")
threads = max(1, int(os.environ.get("GUNICORN_THREADS", "4")))

timeout = int(os.environ.get("GUNICORN_TIMEOUT", "120"))
graceful_timeout = int(os.environ.get("GUNICORN_GRACEFUL_TIMEOUT", "30"))
keepalive = int(os.environ.get("GUNICORN_KEEPALIVE", "5"))

_max_req = os.environ.get("GUNICORN_MAX_REQUESTS")
if _max_req:
    max_requests = int(_max_req)
    max_requests_jitter = int(
        os.environ.get("GUNICORN_MAX_REQUESTS_JITTER", "400")
    )

accesslog = "-"
errorlog = "-"
capture_output = True
