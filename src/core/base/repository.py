"""Abstract Repository Protocol — defines the contract for data access."""
from __future__ import annotations

import uuid
from typing import Generic, Optional, Protocol, TypeVar, runtime_checkable

from core.base.entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


@runtime_checkable
class Repository(Protocol[T]):
    """
    Generic repository interface.

    Application layer depends ONLY on this protocol.
    Infrastructure layer provides the concrete implementation.

    Dependency direction: Infrastructure → Application → Domain (this file)
    """

    def find_by_id(self, id: uuid.UUID) -> Optional[T]:
        """Find an entity by its UUID. Returns None if not found."""
        ...

    def save(self, entity: T) -> T:
        """Persist (insert or update) an entity. Returns the saved entity."""
        ...

    def delete(self, id: uuid.UUID) -> None:
        """Remove an entity by its UUID."""
        ...

    def exists(self, id: uuid.UUID) -> bool:
        """Check if an entity with given id exists."""
        ...


class ListRepository(Repository[T], Protocol[T]):
    """Extended repository with list/search capabilities."""

    def find_all(self, limit: int = 100, offset: int = 0) -> list[T]:
        """Return a paginated list of entities."""
        ...

    def count(self) -> int:
        """Return total count of entities."""
        ...
