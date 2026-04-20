"""User Repository interface — defines the contract for data access."""
from __future__ import annotations

import uuid
from typing import Optional, Protocol, runtime_checkable

from apps.users.domain.entities.user import UserEntity


@runtime_checkable
class UserRepository(Protocol):
    """
    Abstract contract for user persistence.

    Application layer depends on this protocol.
    Infrastructure provides the concrete Django ORM implementation.
    """

    def find_by_id(self, id: uuid.UUID) -> Optional[UserEntity]:
        """Find a user by UUID. Returns None if not found."""
        ...

    def find_by_email(self, email: str) -> Optional[UserEntity]:
        """Find a user by email address. Returns None if not found."""
        ...

    def save(self, user: UserEntity) -> UserEntity:
        """Persist (insert or update) a user entity."""
        ...

    def exists_by_email(self, email: str) -> bool:
        """Check if a user with the given email already exists."""
        ...

    def delete(self, id: uuid.UUID) -> None:
        """Soft-delete a user by UUID."""
        ...

    def list_all(self, offset: int = 0, limit: int = 20) -> list[UserEntity]:
        """List all users with pagination."""
        ...

    def total_count(self) -> int:
        """Return the total number of users."""
        ...
