"""
User Entity — Pure Python domain object.

NO Django imports allowed here.
Business rules live here, persistence is handled by Infrastructure.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from core.base.entity import BaseEntity
from apps.users.domain.value_objects.email import Email
from apps.users.domain.value_objects.full_name import FullName
from apps.users.domain.events.user_registered import UserRegistered
from apps.users.domain.events.user_deactivated import UserDeactivated


@dataclass
class UserEntity(BaseEntity):
    """
    Core User domain entity.

    Business invariants enforced here:
    - Email must be unique (checked at repository level)
    - User can only be deactivated once
    - Admin users have elevated privileges
    """

    email: Email = field(default=None)  # type: ignore[assignment]
    full_name: FullName = field(default=None)  # type: ignore[assignment]
    is_active: bool = True
    is_admin: bool = False

    @classmethod
    def register(
        cls,
        email: str,
        full_name: str,
    ) -> UserEntity:
        """
        Factory method: create a new user and raise UserRegistered event.
        This is the ONLY valid way to create a new user.
        """
        entity = cls(
            email=Email(value=email),
            full_name=FullName(value=full_name),
            is_active=True,
        )
        entity.add_event(UserRegistered(user_id=entity.id, email=email))
        return entity

    def deactivate(self) -> None:
        """Deactivate the user account."""
        if not self.is_active:
            from core.exceptions.base import BusinessRuleException
            raise BusinessRuleException(
                message="User is already deactivated.",
                code="USER_ALREADY_INACTIVE",
            )
        self.is_active = False
        self.touch()
        self.add_event(UserDeactivated(user_id=self.id))

    def activate(self) -> None:
        """Re-activate a deactivated user account."""
        self.is_active = True
        self.touch()

    def update_full_name(self, full_name: str) -> None:
        """Update the user's displayed name."""
        self.full_name = FullName(value=full_name)
        self.touch()

    def __repr__(self) -> str:
        return f"<UserEntity id={self.id} email={self.email.value!r}>"
