"""FullName Value Object."""
from __future__ import annotations

from dataclasses import dataclass

from core.base.value_object import ValueObject
from core.exceptions.base import ValidationException


@dataclass(frozen=True)
class FullName(ValueObject):
    """FullName Value Object — validates length, strips whitespace."""

    value: str

    def _validate(self) -> None:
        stripped = self.value.strip()
        object.__setattr__(self, "value", stripped)
        if len(stripped) < 2:
            raise ValidationException(
                message="Full name must be at least 2 characters.",
                code="INVALID_FULL_NAME",
            )
        if len(stripped) > 150:
            raise ValidationException(
                message="Full name cannot exceed 150 characters.",
                code="FULL_NAME_TOO_LONG",
            )

    def __str__(self) -> str:
        return self.value
