from collections import defaultdict, deque
from time import monotonic

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 120):
        super().__init__(app)
        self.requests_per_minute = max(1, requests_per_minute)
        self.window_seconds = 60
        self.hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client_host = request.client.host if request.client else "unknown"
        key = f"{client_host}:{request.url.path}"
        now = monotonic()
        bucket = self.hits[key]
        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()
        if len(bucket) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please try again shortly."},
            )
        bucket.append(now)
        return await call_next(request)
