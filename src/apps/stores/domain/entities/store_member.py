"""
StoreMember Entity — Domain object for Many-to-Many membership.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from core.base.entity import BaseEntity
from apps.stores.domain.value_objects.role import StoreRole


@dataclass
class StoreMemberEntity(BaseEntity):
    """
    Represents a User's membership in a Store.
    """

    user_id: uuid.UUID = field(default_factory=uuid.uuid4)
    store_id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: StoreRole = field(default=StoreRole.STAFF)

    def change_role(self, new_role: StoreRole) -> None:
        """Change the member's role."""
        if self.role == StoreRole.OWNER and new_role != StoreRole.OWNER:
            # Logic for ownership transfer should probably be in a service
            pass
        self.role = new_role
        self.touch()

    def __repr__(self) -> str:
        return f"<StoreMemberEntity user={self.user_id} store={self.store_id} role={self.role}>"
