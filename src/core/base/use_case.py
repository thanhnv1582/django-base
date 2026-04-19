"""Abstract Use Case — application service contract."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class UseCase(ABC, Generic[InputDTO, OutputDTO]):
    """
    Base class for all application use cases.

    Each use case encapsulates a single business operation.
    Business logic MUST live here, NOT in Views or Models.

    Pattern:
        use_case = RegisterUserUseCase(repo=..., uow=...)
        result = use_case.execute(RegisterUserInput(...))
    """

    @abstractmethod
    def execute(self, input_dto: InputDTO) -> OutputDTO:
        """Execute the use case with the given input and return output."""
        raise NotImplementedError
