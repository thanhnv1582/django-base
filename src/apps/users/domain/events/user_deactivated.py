"""UserDeactivated domain event."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from core.base.domain_event import DomainEvent


@dataclass(frozen=True)
class UserDeactivated(DomainEvent):
    """Raised when a user account is deactivated."""

    user_id: uuid.UUID = field(default=None)  # type: ignore[assignment]
