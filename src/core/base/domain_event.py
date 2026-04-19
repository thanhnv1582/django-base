"""Base Domain Event."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class DomainEvent:
    """
    Base class for all domain events.

    Domain events represent something that happened in the domain.
    They are immutable facts, raised by Entities and dispatched after
    successful persistence.
    """

    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )

    @property
    def event_type(self) -> str:
        """Return the fully-qualified event class name."""
        return f"{self.__class__.__module__}.{self.__class__.__name__}"
