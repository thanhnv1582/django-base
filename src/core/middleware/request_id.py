"""Request ID middleware — inject X-Request-ID into every request/response."""
from __future__ import annotations

import uuid

from django.http import HttpRequest, HttpResponse


class RequestIdMiddleware:
    """
    Injects a unique X-Request-ID header into every request and response.

    - Reads X-Request-ID from incoming request (if client provides one)
    - Falls back to generated UUID if not present
    - Attaches request_id as request.request_id attribute
    - Echoes the ID back in the response header

    Useful for distributed tracing and log correlation.
    """

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
        request.request_id = request_id  # type: ignore[attr-defined]

        response = self.get_response(request)
        response["X-Request-Id"] = request_id
        return response
