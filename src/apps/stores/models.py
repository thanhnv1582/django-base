"""
Store ORM Models.
Standard location for Django model discovery.
"""
from django.db import models
from django.utils.text import slugify

from core.base.model import UUIDModel, SoftDeleteModel
from apps.stores.domain.entities.store import StoreEntity
from apps.stores.domain.entities.store_member import StoreMemberEntity
from apps.stores.domain.value_objects.role import StoreRole


class Store(UUIDModel, SoftDeleteModel):
    """Store ORM Model."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    logo = models.URLField(max_length=500, blank=True, null=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "stores"
        db_table = "stores"
        verbose_name = "store"
        verbose_name_plural = "stores"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def to_domain(self) -> StoreEntity:
        return StoreEntity(
            id=self.id,
            name=self.name,
            slug=self.slug,
            description=self.description,
            logo=self.logo,
            address=self.address,
            phone=self.phone,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return self.name


class StoreMember(UUIDModel):
    """Store Member ORM Model (Join table)."""

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="store_memberships")
    role = models.CharField(
        max_length=20,
        choices=StoreRole.choices(),
        default=StoreRole.STAFF.value
    )

    class Meta:
        app_label = "stores"
        db_table = "store_members"
        unique_together = ("store", "user")
        verbose_name = "store member"
        verbose_name_plural = "store members"

    def to_domain(self) -> StoreMemberEntity:
        return StoreMemberEntity(
            id=self.id,
            store_id=self.store_id,
            user_id=self.user_id,
            role=StoreRole(self.role),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return f"{self.user} at {self.store} ({self.role})"
