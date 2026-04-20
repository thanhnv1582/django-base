"""
Store Repository Interface.
"""
from __future__ import annotations

import uuid
from typing import Optional, Protocol, List

from apps.stores.domain.entities.store import StoreEntity
from apps.stores.domain.entities.store_member import StoreMemberEntity


class IStoreRepository(Protocol):
    """
    Interface for store persistence.
    """

    def save(self, store: StoreEntity) -> None:
        """Persist a store."""
        ...

    def get_by_id(self, store_id: uuid.UUID) -> Optional[StoreEntity]:
        """Retrieve a store by ID."""
        ...

    def get_by_slug(self, slug: str) -> Optional[StoreEntity]:
        """Retrieve a store by slug."""
        ...

    def list_all(self, is_active: Optional[bool] = None) -> List[StoreEntity]:
        """List all stores."""
        ...

    def save_member(self, member: StoreMemberEntity) -> None:
        """Persist a store member."""
        ...

    def get_members(self, store_id: uuid.UUID) -> List[StoreMemberEntity]:
        """List members of a store."""
        ...

    def get_user_stores(self, user_id: uuid.UUID) -> List[StoreEntity]:
        """List stores a user belongs to."""
        ...
