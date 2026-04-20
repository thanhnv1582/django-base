"""
Store Entity — Pure Python domain object.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from core.base.entity import BaseEntity


@dataclass
class StoreEntity(BaseEntity):
    """
    Core Store domain entity.
    """

    name: str = field(default="")
    slug: str = field(default="")
    description: str = field(default="")
    logo: Optional[str] = field(default=None)
    address: str = field(default="")
    phone: str = field(default="")
    is_active: bool = True

    def activate(self) -> None:
        """Activate the store."""
        self.is_active = True
        self.touch()

    def deactivate(self) -> None:
        """Deactivate the store."""
        self.is_active = False
        self.touch()

    def update_info(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        logo: Optional[str] = None,
    ) -> None:
        """Update store information."""
        if name:
            self.name = name
        if description is not None:
            self.description = description
        if address:
            self.address = address
        if phone:
            self.phone = phone
        if logo:
            self.logo = logo
        self.touch()

    def __repr__(self) -> str:
        return f"<StoreEntity id={self.id} name={self.name!r}>"
