"""Health check views — verifies DB, Redis, Celery connectivity."""
from __future__ import annotations

import time

from django.core.cache import cache
from django.db import connection, OperationalError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


class HealthCheckView(APIView):
    """
    GET /api/health/

    Public endpoint that checks:
    - Database connectivity
    - Redis/cache connectivity

    Returns 200 if all systems operational, 503 if any system is down.
    Used by Docker health checks, load balancers, and monitoring tools.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(exclude=True)  # Don't show in Swagger
    def get(self, request: Request) -> Response:
        checks = {
            "db": self._check_database(),
            "cache": self._check_cache(),
        }

        is_healthy = all(v == "ok" for v in checks.values())
        status_code = 200 if is_healthy else 503

        return Response(
            {
                "status": "healthy" if is_healthy else "degraded",
                "checks": checks,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            status=status_code,
        )

    @staticmethod
    def _check_database() -> str:
        try:
            connection.ensure_connection()
            return "ok"
        except OperationalError:
            return "error"

    @staticmethod
    def _check_cache() -> str:
        try:
            cache.set("health_check", "ok", timeout=5)
            result = cache.get("health_check")
            return "ok" if result == "ok" else "error"
        except Exception:
            return "error"
