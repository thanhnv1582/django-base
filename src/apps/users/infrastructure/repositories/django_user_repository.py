"""
Django ORM implementation of UserRepository.

Translates between UserEntity (domain) and User (ORM).
This is the ONLY place where Django ORM touches domain objects.
"""
from __future__ import annotations

import uuid
from typing import Optional

from apps.users.domain.entities.user import UserEntity
from apps.users.domain.repositories.user_repository import UserRepository
from apps.users.domain.value_objects.email import Email
from apps.users.domain.value_objects.full_name import FullName
from apps.users.infrastructure.models.user_model import User


class DjangoUserRepository:
    """
    Concrete implementation of UserRepository using Django ORM.

    Mapping responsibilities:
    - model → entity: _to_entity()
    - entity → model: _to_model()
    """

    def find_by_id(self, id: uuid.UUID) -> Optional[UserEntity]:
        try:
            model = User.objects.get(id=id)
            return self._to_entity(model)
        except User.DoesNotExist:
            return None

    def find_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            model = User.objects.get(email=email.lower().strip())
            return self._to_entity(model)
        except User.DoesNotExist:
            return None

    def exists_by_email(self, email: str) -> bool:
        return User.objects.filter(email=email.lower().strip()).exists()

    def save(self, user: UserEntity, password: str | None = None) -> UserEntity:
        """
        Persist UserEntity to the database.
        If password is provided, it will be hashed via set_password().
        """
        try:
            model = User.objects.get(id=user.id)
        except User.DoesNotExist:
            model = User(id=user.id)

        model.email = user.email.value
        model.full_name = user.full_name.value
        model.is_active = user.is_active
        model.is_admin = user.is_admin

        if password:
            model.set_password(password)

        model.save()
        return self._to_entity(model)

    def delete(self, id: uuid.UUID) -> None:
        """Soft-delete by UUID."""
        User.objects.filter(id=id).update(is_deleted=True)

    # ── Private mapping helpers ───────────────────────────────────────────────

    @staticmethod
    def _to_entity(model: User) -> UserEntity:
        """Map ORM model → domain entity."""
        entity = UserEntity(
            id=model.id,
            email=Email(value=model.email),
            full_name=FullName(value=model.full_name),
            is_active=model.is_active,
            is_admin=model.is_admin,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return entity
