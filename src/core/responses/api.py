"""Unified API response format — success and error."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any


def success_response(
    data: Any = None,
    message: str | None = None,
    meta: dict | None = None,
    request_id: str | None = None,
) -> dict:
    """
    Standard success response envelope.

    Example:
        {
            "success": true,
            "message": "User created successfully.",
            "data": { "id": "...", "email": "..." },
            "meta": { "page": 1, "total": 100 },
            "request_id": "abc-123",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta or {},
        "request_id": request_id or str(uuid.uuid4()),
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


def error_response(
    code: str,
    message: str,
    details: dict | None = None,
    request_id: str | None = None,
) -> dict:
    """
    Standard error response envelope.

    Example:
        {
            "success": false,
            "error": {
                "code": "USER_NOT_FOUND",
                "message": "User does not exist.",
                "details": {}
            },
            "request_id": "abc-123",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    """
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
        "request_id": request_id or str(uuid.uuid4()),
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }
