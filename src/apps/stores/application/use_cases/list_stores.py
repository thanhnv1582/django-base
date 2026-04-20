from core.base.use_case import UseCase
from apps.stores.domain.repositories.store_repository import IStoreRepository
from apps.stores.application.dtos.store_dtos import StoreReadDTO
from typing import List

class ListStoresUseCase(UseCase[None, List[StoreReadDTO]]):
    """UseCase for listing all stores (for dashboard)."""

    def __init__(self, store_repo: IStoreRepository):
        self.store_repo = store_repo

    def execute(self, input_dto: None = None) -> List[StoreReadDTO]:
        stores = self.store_repo.list_all()
        return [
            StoreReadDTO(
                id=s.id,
                name=s.name,
                slug=s.slug,
                description=s.description,
                address=s.address,
                phone=s.phone,
                logo=s.logo,
                is_active=s.is_active,
                created_at=s.created_at.isoformat()
            )
            for s in stores
        ]
