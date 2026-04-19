"""
DRF Serializers for Users v1 — input validation and output formatting only.

RULES:
- Serializers do NOT contain business logic
- They only validate request format and shape the response
- Business logic lives in Use Cases (application layer)
"""
from __future__ import annotations

from rest_framework import serializers


class RegisterUserSerializer(serializers.Serializer):
    """Validates the registration request payload."""

    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True,
        style={"input_type": "password"},
    )
    full_name = serializers.CharField(min_length=2, max_length=150)


class UserOutputSerializer(serializers.Serializer):
    """Formats the UserOutput DTO for HTTP response."""

    id = serializers.UUIDField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    is_active = serializers.BooleanField()
    is_admin = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class UpdateProfileSerializer(serializers.Serializer):
    """Validates the profile update request payload."""

    full_name = serializers.CharField(min_length=2, max_length=150)
