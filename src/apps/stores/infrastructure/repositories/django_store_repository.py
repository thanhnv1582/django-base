"""
Django implementation of IStoreRepository.
"""
from __future__ import annotations

import uuid
from typing import List, Optional

from apps.stores.domain.entities.store import StoreEntity
from apps.stores.domain.entities.store_member import StoreMemberEntity
from apps.stores.domain.repositories.store_repository import IStoreRepository
from apps.stores.infrastructure.models.store_model import Store, StoreMember


class DjangoStoreRepository(IStoreRepository):
    """
    Store repository using Django ORM.
    """

    def save(self, store: StoreEntity) -> None:
        """Persist a store."""
        defaults = {
            "name": store.name,
            "slug": store.slug,
            "description": store.description,
            "logo": store.logo,
            "address": store.address,
            "phone": store.phone,
            "is_active": store.is_active,
        }
        Store.objects.update_or_create(id=store.id, defaults=defaults)

    def get_by_id(self, store_id: uuid.UUID) -> Optional[StoreEntity]:
        """Retrieve a store by ID."""
        try:
            model = Store.objects.get(id=store_id)
            return model.to_domain()
        except Store.DoesNotExist:
            return None

    def get_by_slug(self, slug: str) -> Optional[StoreEntity]:
        """Retrieve a store by slug."""
        try:
            model = Store.objects.get(slug=slug)
            return model.to_domain()
        except Store.DoesNotExist:
            return None

    def list_all(self, is_active: Optional[bool] = None) -> List[StoreEntity]:
        """List all stores."""
        queryset = Store.objects.all()
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        return [model.to_domain() for model in queryset]

    def save_member(self, member: StoreMemberEntity) -> None:
        """Persist a store member."""
        defaults = {
            "role": member.role.value,
        }
        StoreMember.objects.update_or_create(
            store_id=member.store_id,
            user_id=member.user_id,
            defaults=defaults
        )

    def get_members(self, store_id: uuid.UUID) -> List[StoreMemberEntity]:
        """List members of a store."""
        queryset = StoreMember.objects.filter(store_id=store_id)
        return [model.to_domain() for model in queryset]

    def get_user_stores(self, user_id: uuid.UUID) -> List[StoreEntity]:
        """List stores a user belongs to."""
        stores = Store.objects.filter(members__user_id=user_id)
        return [model.to_domain() for model in stores]
