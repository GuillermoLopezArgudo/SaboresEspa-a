"""Rate limit en memoria (por proceso).

Con gunicorn multi-worker el límite no es global. En Render usamos 1 worker
(+ threads) para que este contador sea coherente sin Redis.
"""

import time
from collections import defaultdict, deque
from functools import wraps
from threading import Lock

from flask import jsonify, request

_lock = Lock()
_hits: dict[str, deque] = defaultdict(deque)


def _client_key(prefix: str) -> str:
    forwarded = request.headers.get("X-Forwarded-For", "")
    ip = forwarded.split(",")[0].strip() if forwarded else (request.remote_addr or "unknown")
    return f"{prefix}:{ip}"


def rate_limit(max_calls: int, window_seconds: int, prefix: str = "auth"):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = _client_key(prefix)
            now = time.time()
            with _lock:
                q = _hits[key]
                while q and q[0] <= now - window_seconds:
                    q.popleft()
                if len(q) >= max_calls:
                    return (
                        jsonify(
                            message="Demasiados intentos. Espera unos minutos e inténtalo de nuevo."
                        ),
                        429,
                    )
                q.append(now)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
