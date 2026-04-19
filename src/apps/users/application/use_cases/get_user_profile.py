"""GetUserProfile Use Case."""
from __future__ import annotations

import uuid

from core.base.use_case import UseCase
from core.exceptions.base import NotFoundException
from apps.users.domain.repositories.user_repository import UserRepository
from apps.users.application.dtos.user_dto import UserOutput


class GetUserProfileUseCase(UseCase[uuid.UUID, UserOutput]):
    """
    Use Case: Retrieve a user's profile by ID.

    Raises:
        NotFoundException: If user does not exist.
    """

    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def execute(self, input_dto: uuid.UUID) -> UserOutput:
        user = self._repo.find_by_id(id=input_dto)
        if user is None:
            raise NotFoundException(
                message=f"User with id '{input_dto}' not found.",
                code="USER_NOT_FOUND",
            )
        return UserOutput.from_entity(user)
