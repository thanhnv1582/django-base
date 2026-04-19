"""Application-level exception hierarchy."""
from __future__ import annotations

from http import HTTPStatus


class AppException(Exception):
    """
    Base exception for all application-level errors.

    All domain and application exceptions should inherit from this.
    The global exception handler converts these to unified JSON responses.
    """

    code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred."
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message: str | None = None,
        code: str | None = None,
        details: dict | None = None,
    ) -> None:
        self.message = message or self.__class__.message
        self.code = code or self.__class__.code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


class ValidationException(AppException):
    """Raised when input validation fails (400 Bad Request)."""

    code = "VALIDATION_ERROR"
    message = "Validation failed."
    status_code = HTTPStatus.BAD_REQUEST


class NotFoundException(AppException):
    """Raised when a requested resource does not exist (404)."""

    code = "NOT_FOUND"
    message = "Resource not found."
    status_code = HTTPStatus.NOT_FOUND


class AuthenticationException(AppException):
    """Raised when authentication fails (401)."""

    code = "AUTHENTICATION_FAILED"
    message = "Authentication credentials were not provided or are invalid."
    status_code = HTTPStatus.UNAUTHORIZED


class PermissionException(AppException):
    """Raised when user lacks permission to perform an action (403)."""

    code = "PERMISSION_DENIED"
    message = "You do not have permission to perform this action."
    status_code = HTTPStatus.FORBIDDEN


class ConflictException(AppException):
    """Raised when a resource conflict occurs (409), e.g. duplicate email."""

    code = "CONFLICT"
    message = "Resource conflict."
    status_code = HTTPStatus.CONFLICT


class BusinessRuleException(AppException):
    """Raised when a domain business rule is violated (422)."""

    code = "BUSINESS_RULE_VIOLATED"
    message = "Business rule violation."
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class ExternalServiceException(AppException):
    """Raised when an external service (email, S3, SMS) fails (502)."""

    code = "EXTERNAL_SERVICE_ERROR"
    message = "External service unavailable."
    status_code = HTTPStatus.BAD_GATEWAY
