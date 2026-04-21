from rest_framework import serializers
from apps.vouchers.models import Voucher

class VoucherSerializer(serializers.ModelSerializer):
    """Serializer for Voucher model."""

    class Meta:
        model = Voucher
        fields = [
            "id",
            "store",
            "code",
            "voucher_type",
            "value",
            "min_order_value",
            "max_discount_amount",
            "usage_limit",
            "usage_per_user",
            "current_usage",
            "start_date",
            "end_date",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "current_usage", "created_at", "updated_at"]
