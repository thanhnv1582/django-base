"""Email Value Object — validates format on construction."""
from __future__ import annotations

import re
from dataclasses import dataclass

from core.base.value_object import ValueObject
from core.exceptions.base import ValidationException

_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


@dataclass(frozen=True)
class Email(ValueObject):
    """
    Email Value Object.

    Guarantees:
    - Value is a syntactically valid email address
    - Stored in lowercase, stripped of whitespace
    """

    value: str

    def _validate(self) -> None:
        normalized = self.value.strip().lower()
        # frozen=True means we can't reassign, use object.__setattr__
        object.__setattr__(self, "value", normalized)
        if not _EMAIL_REGEX.match(normalized):
            raise ValidationException(
                message=f"'{self.value}' is not a valid email address.",
                code="INVALID_EMAIL",
            )

    def __str__(self) -> str:
        return self.value
