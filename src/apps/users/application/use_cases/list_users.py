"""Use case for listing all users with pagination."""
from __future__ import annotations

from apps.users.application.dtos.user_dto import ListUsersInput, PaginatedUserOutput, UserOutput
from apps.users.domain.repositories.user_repository import UserRepository
from core.base.use_case import UseCase


class ListUsersUseCase(UseCase[ListUsersInput, PaginatedUserOutput]):
    """
    Retrieves a paginated list of users from the repository.
    Used primarily for the administrative dashboard.
    """

    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def execute(self, input_dto: ListUsersInput) -> PaginatedUserOutput:
        offset = (input_dto.page - 1) * input_dto.page_size
        
        users = self._repo.list_all(offset=offset, limit=input_dto.page_size)
        total = self._repo.total_count()
        
        return PaginatedUserOutput(
            items=[UserOutput.from_entity(u) for u in users],
            total=total,
            page=input_dto.page,
            page_size=input_dto.page_size,
        )
