"""Request logging middleware — structured logs for every HTTP request."""
from __future__ import annotations

import logging
import time

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("core.access")


class RequestLoggingMiddleware:
    """
    Logs every incoming request with method, path, status, duration.

    Log format (JSON-compatible via structlog):
        method=GET path=/api/v1/users/ status=200 duration=0.045s request_id=abc-123
    """

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.perf_counter()
        request_id = getattr(request, "request_id", "-")

        response = self.get_response(request)

        duration = time.perf_counter() - start_time
        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration": f"{duration:.4f}s",
                "request_id": request_id,
                "user": getattr(request.user, "id", "anonymous"),
            },
        )
        return response
