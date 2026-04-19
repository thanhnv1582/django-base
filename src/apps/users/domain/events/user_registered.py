"""UserRegistered domain event."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from core.base.domain_event import DomainEvent


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    """Raised when a new user successfully registers."""

    user_id: uuid.UUID = field(default=None)  # type: ignore[assignment]
    email: str = field(default="")
