"""RegisterUser Use Case — orchestrates user registration."""
from __future__ import annotations

from core.base.use_case import UseCase
from core.exceptions.base import ConflictException
from apps.users.domain.entities.user import UserEntity
from apps.users.domain.repositories.user_repository import UserRepository
from apps.users.application.dtos.user_dto import RegisterUserInput, UserOutput
from apps.users.application.services.unit_of_work import UnitOfWork


class RegisterUserUseCase(UseCase[RegisterUserInput, UserOutput]):
    """
    Use Case: Register a new user.

    Business steps:
    1. Check email uniqueness
    2. Create UserEntity via factory method (raises domain event)
    3. Persist via repository inside UoW transaction
    4. Return UserOutput DTO

    Raises:
        ConflictException: If email already exists.
        ValidationException: If email or full_name has invalid format.
    """

    def __init__(self, repo: UserRepository, uow: UnitOfWork) -> None:
        self._repo = repo
        self._uow = uow

    def execute(self, input_dto: RegisterUserInput) -> UserOutput:
        # Step 1: Check email uniqueness (business rule)
        if self._repo.exists_by_email(email=input_dto.email):
            raise ConflictException(
                message=f"A user with email '{input_dto.email}' already exists.",
                code="EMAIL_ALREADY_REGISTERED",
            )

        # Step 2: Create domain entity (validates VOs, raises domain event)
        user = UserEntity.register(
            email=input_dto.email,
            full_name=input_dto.full_name,
        )

        # Step 3: Persist inside transaction
        with self._uow.atomic():
            # Set hashed password — handled by Django's User model
            saved_user = self._repo.save(user, password=input_dto.password)

        # Step 4: (Optional) dispatch domain events to event bus
        # event_bus.publish(saved_user.pull_events())

        return UserOutput.from_entity(saved_user)
