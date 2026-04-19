"""Base Value Object — immutable, equality by value."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    """
    Base class for all Value Objects.

    Rules:
    - Immutable (frozen dataclass)
    - Equality determined by attribute values, not identity
    - Should validate their own invariants in __post_init__
    - No Django imports — pure Python
    """

    def __post_init__(self) -> None:
        """Override to add validation logic."""
        self._validate()

    def _validate(self) -> None:
        """Override in subclasses to validate invariants."""
