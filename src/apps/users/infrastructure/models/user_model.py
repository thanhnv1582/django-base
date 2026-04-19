"""
Django ORM User model — persistence layer only.

This model is the INFRASTRUCTURE representation of the User domain entity.
Business logic belongs in UserEntity, NOT here.
"""
from __future__ import annotations

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from core.base.model import SoftDeleteModel, UUIDModel


class UserModelManager(BaseUserManager):
    """Custom manager for User model."""

    def create_user(self, email: str, password: str | None = None, **extra_fields) -> "UserModel":
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> "UserModel":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        return self.create_user(email, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin, UUIDModel, SoftDeleteModel):
    """
    Django ORM User model.

    Extends AbstractBaseUser (auth), PermissionsMixin (groups/permissions),
    UUIDModel (UUID pk), SoftDeleteModel (soft delete support).
    """

    email = models.EmailField(unique=True, db_index=True)
    full_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserModelManager()

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return self.email
