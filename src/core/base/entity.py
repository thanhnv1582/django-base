"""Base Entity class — the root aggregate for all domain entities."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.base.domain_event import DomainEvent


def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


@dataclass
class BaseEntity:
    """
    Base class for all domain entities.

    Rules:
    - Identity is determined by `id`, not by attribute equality
    - Entities carry domain events raised during lifecycle changes
    - No Django imports — this is pure Python
    """

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    _domain_events: list["DomainEvent"] = field(default_factory=list, repr=False, compare=False)

    def add_event(self, event: "DomainEvent") -> None:
        """Register a domain event to be dispatched after persistence."""
        self._domain_events.append(event)

    def pull_events(self) -> list["DomainEvent"]:
        """Retrieve and clear all pending domain events."""
        events = list(self._domain_events)
        self._domain_events.clear()
        return events

    def touch(self) -> None:
        """Update the `updated_at` timestamp."""
        self.updated_at = utcnow()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
