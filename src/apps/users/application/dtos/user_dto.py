"""DTOs for the Users application layer."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime


# ─── Input DTOs (what comes IN from the presentation layer) ───────────────────

@dataclass(frozen=True)
class RegisterUserInput:
    """Input for RegisterUserUseCase."""
    email: str
    password: str
    full_name: str


@dataclass(frozen=True)
class UpdateProfileInput:
    """Input for UpdateProfileUseCase."""
    user_id: uuid.UUID
    full_name: str


@dataclass(frozen=True)
class ChangePasswordInput:
    """Input for ChangePasswordUseCase."""
    user_id: uuid.UUID
    current_password: str
    new_password: str


# ─── Output DTOs (what goes OUT to the presentation layer) ────────────────────

@dataclass(frozen=True)
class UserOutput:
    """Represents a user returned to the client."""
    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, user) -> UserOutput:
        """Map from UserEntity to output DTO."""
        from apps.users.domain.entities.user import UserEntity
        assert isinstance(user, UserEntity)
        return cls(
            id=user.id,
            email=user.email.value,
            full_name=user.full_name.value,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
