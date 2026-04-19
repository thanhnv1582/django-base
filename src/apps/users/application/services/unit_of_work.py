"""Unit of Work — manages transaction boundaries."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from django.db import transaction


class UnitOfWork:
    """
    Unit of Work pattern for managing atomic transactions.

    Ensures that all repository operations within a use case
    are committed or rolled back as a single unit.

    Usage:
        uow = UnitOfWork()
        with uow.atomic():
            user = repo.save(user_entity)
            # If exception occurs, everything rolls back
    """

    @contextmanager
    def atomic(self) -> Generator[None, None, None]:
        """Context manager for atomic database transaction."""
        with transaction.atomic():
            yield

    def savepoint(self):
        """Create a savepoint for nested transaction control."""
        return transaction.savepoint()

    def savepoint_rollback(self, sid) -> None:
        """Roll back to a savepoint."""
        transaction.savepoint_rollback(sid)

    def savepoint_commit(self, sid) -> None:
        """Release a savepoint."""
        transaction.savepoint_commit(sid)
