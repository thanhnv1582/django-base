from rest_framework import serializers
from apps.stores.infrastructure.models.store_model import Store, StoreMember

class StoreSerializer(serializers.ModelSerializer):
    """Serializer for Store model."""

    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "logo",
            "address",
            "phone",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

class StoreMemberSerializer(serializers.ModelSerializer):
    """Serializer for StoreMember model."""
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = StoreMember
        fields = ["id", "user", "user_email", "user_name", "role", "created_at"]
        read_only_fields = ["id", "created_at"]
