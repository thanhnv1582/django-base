"""Use case for toggling a user's active status."""
from __future__ import annotations

import uuid
from dataclasses import dataclass

from apps.users.application.dtos.user_dto import UserOutput
from apps.users.application.services.unit_of_work import UnitOfWork
from apps.users.domain.repositories.user_repository import UserRepository
from core.base.use_case import UseCase
from core.exceptions.base import NotFoundException


@dataclass(frozen=True)
class ToggleUserStatusInput:
    user_id: uuid.UUID


class ToggleUserStatusUseCase(UseCase[ToggleUserStatusInput, UserOutput]):
    """
    Toggles is_active status of a user.
    Used for quick administrative actions.
    """

    def __init__(self, repo: UserRepository, uow: UnitOfWork) -> None:
        self._repo = repo
        self._uow = uow

    def execute(self, input_dto: ToggleUserStatusInput) -> UserOutput:
        with self._uow:
            user = self._repo.find_by_id(input_dto.user_id)
            if not user:
                raise NotFoundException(f"User {input_dto.user_id} not found.")

            if user.is_active:
                user.deactivate()
            else:
                user.activate()

            updated_user = self._repo.save(user)
            self._uow.commit()
            
            return UserOutput.from_entity(updated_user)
