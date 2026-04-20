from typing import Optional
from django.utils.text import slugify

from core.base.use_case import UseCase
from apps.stores.application.dtos.store_dtos import StoreCreateDTO, StoreReadDTO
from apps.stores.domain.entities.store import StoreEntity
from apps.stores.domain.entities.store_member import StoreMemberEntity
from apps.stores.domain.repositories.store_repository import IStoreRepository
from apps.stores.domain.value_objects.role import StoreRole
import uuid

class CreateStoreUseCase(UseCase[StoreCreateDTO, StoreReadDTO]):
    """
    UseCase for creating a new store.
    The creator is automatically added as the OWNER.
    """

    def __init__(self, store_repo: IStoreRepository):
        self.store_repo = store_repo

    def execute(self, input_dto: StoreCreateDTO, user_id: uuid.UUID) -> StoreReadDTO:
        # 1. Create Store Entity
        store = StoreEntity(
            name=input_dto.name,
            slug=slugify(input_dto.name),
            description=input_dto.description,
            address=input_dto.address,
            phone=input_dto.phone,
            logo=input_dto.logo,
            is_active=True
        )

        # 2. Save Store
        self.store_repo.save(store)

        # 3. Create Ownership Member
        member = StoreMemberEntity(
            user_id=user_id,
            store_id=store.id,
            role=StoreRole.OWNER
        )
        self.store_repo.save_member(member)

        # 4. Return Read DTO
        return StoreReadDTO(
            id=store.id,
            name=store.name,
            slug=store.slug,
            description=store.description,
            address=store.address,
            phone=store.phone,
            logo=store.logo,
            is_active=store.is_active,
            created_at=store.created_at.isoformat()
        )
