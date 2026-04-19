"""Base Django ORM models — TimestampedModel and SoftDeleteModel."""
from __future__ import annotations

import uuid
from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    """
    Abstract model with created_at and updated_at auto-timestamps.

    Inherit from this for all Django ORM persistence models.
    """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract model with UUID primary key instead of auto-increment int."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet that hides soft-deleted records by default."""

    def delete(self) -> tuple[int, dict]:
        """Override bulk delete to use soft delete."""
        return self.update(deleted_at=timezone.now(), is_deleted=True), {}

    def hard_delete(self) -> tuple[int, dict]:
        """Physically remove records from the database."""
        return super().delete()

    def alive(self) -> SoftDeleteQuerySet:
        """Return only non-deleted records."""
        return self.filter(is_deleted=False)

    def dead(self) -> SoftDeleteQuerySet:
        """Return only soft-deleted records."""
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    """Custom manager that excludes soft-deleted records by default."""

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def all_with_deleted(self) -> SoftDeleteQuerySet:
        """Return all records including soft-deleted ones."""
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDeleteModel(TimestampedModel):
    """
    Abstract model with soft delete capability.

    Records are never physically deleted — they are marked with
    deleted_at timestamp and excluded from default queries.
    """

    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Access all records including deleted

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False) -> None:
        """Soft delete: set deleted_at and is_deleted flag."""
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save(update_fields=["deleted_at", "is_deleted"])

    def hard_delete(self, using=None, keep_parents=False) -> None:
        """Physical delete — use with caution."""
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self) -> None:
        """Undo a soft delete."""
        self.deleted_at = None
        self.is_deleted = False
        self.save(update_fields=["deleted_at", "is_deleted"])
