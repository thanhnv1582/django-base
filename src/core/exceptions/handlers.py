"""
Global DRF exception handler.

Converts ALL exceptions — Django, DRF, and domain AppExceptions —
into a unified JSON response format.

Configured in settings.py:
    REST_FRAMEWORK = {
        "EXCEPTION_HANDLER": "core.exceptions.handlers.global_exception_handler"
    }
"""
from __future__ import annotations

import logging
import uuid
from http import HTTPStatus

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied as DRFPermissionDenied,
    ValidationError as DRFValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from core.exceptions.base import AppException

logger = logging.getLogger(__name__)


def _build_error_response(
    code: str,
    message: str,
    details: dict,
    status_code: int,
    request_id: str,
) -> Response:
    """Build the standardized error response body."""
    from core.responses.api import error_response

    return Response(
        error_response(code=code, message=message, details=details, request_id=request_id),
        status=status_code,
    )


def global_exception_handler(exc: Exception, context: dict) -> Response | None:
    """
    Centralized exception handler for all DRF views.

    Priority:
    1. AppException subclasses (domain/application errors)
    2. DRF built-in exceptions
    3. Django exceptions (Http404, PermissionDenied, ValidationError)
    4. Unknown exceptions → 500
    """
    request = context.get("request")
    request_id = getattr(request, "request_id", str(uuid.uuid4()))

    # ── 1. Application / Domain exceptions ────────────────────────────────────
    if isinstance(exc, AppException):
        logger.warning(
            "AppException",
            extra={"code": exc.code, "message": exc.message, "request_id": request_id},
        )
        return _build_error_response(
            code=exc.code,
            message=exc.message,
            details=exc.details,
            status_code=exc.status_code,
            request_id=request_id,
        )

    # ── 2. Map Django exceptions → DRF equivalents ────────────────────────────
    if isinstance(exc, Http404):
        exc = DRFValidationError(detail="Not found.")
        exc.status_code = HTTPStatus.NOT_FOUND

    elif isinstance(exc, PermissionDenied):
        exc = DRFPermissionDenied()

    # ── 3. Let DRF handle its own exceptions first ────────────────────────────
    response = drf_exception_handler(exc, context)

    if response is not None:
        code, message, details = _parse_drf_exception(exc, response)
        return _build_error_response(
            code=code,
            message=message,
            details=details,
            status_code=response.status_code,
            request_id=request_id,
        )

    # ── 4. Unhandled exception → 500 ─────────────────────────────────────────
    logger.exception(
        "Unhandled server error",
        exc_info=exc,
        extra={"request_id": request_id},
    )
    return _build_error_response(
        code="INTERNAL_ERROR",
        message="An unexpected error occurred. Please try again.",
        details={},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        request_id=request_id,
    )


def _parse_drf_exception(exc, response: Response) -> tuple[str, str, dict]:
    """Extract code, message, details from DRF exception."""
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return "AUTHENTICATION_FAILED", "Authentication credentials are invalid.", {}

    if isinstance(exc, DRFPermissionDenied):
        return "PERMISSION_DENIED", "You do not have permission to perform this action.", {}

    if isinstance(exc, DRFValidationError):
        details = _flatten_validation_errors(response.data)
        return "VALIDATION_ERROR", "Validation failed.", details

    # Generic DRF exception
    detail = response.data.get("detail", str(exc))
    return "API_ERROR", str(detail), {}


def _flatten_validation_errors(data: dict | list | str) -> dict:
    """Flatten nested DRF validation errors into a flat dict."""
    if isinstance(data, str):
        return {"non_field_errors": [data]}
    if isinstance(data, list):
        return {"non_field_errors": [str(e) for e in data]}
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, list):
                result[key] = [str(e) for e in value]
            else:
                result[key] = str(value)
        return result
    return {}
