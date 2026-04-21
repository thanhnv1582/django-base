"""
Voucher ORM Models.
"""
from django.db import models
from core.base.model import UUIDModel, SoftDeleteModel
from apps.vouchers.domain.entities.voucher import VoucherEntity
from apps.vouchers.domain.value_objects.voucher_type import VoucherType

class Voucher(UUIDModel, SoftDeleteModel):
    """Voucher ORM Model."""

    store = models.ForeignKey(
        "stores.Store", 
        on_delete=models.CASCADE, 
        related_name="vouchers"
    )
    code = models.CharField(max_length=50, db_index=True)
    voucher_type = models.CharField(
        max_length=20,
        choices=VoucherType.choices(),
        default=VoucherType.FIXED.value
    )
    value = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Limits
    min_order_value = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    max_discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    usage_limit = models.PositiveIntegerField(default=0)
    usage_per_user = models.PositiveIntegerField(default=1)
    current_usage = models.PositiveIntegerField(default=0)
    
    # Validity
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "vouchers"
        db_table = "vouchers"
        verbose_name = "voucher"
        verbose_name_plural = "vouchers"
        unique_together = ("store", "code")
        ordering = ["-created_at"]

    def to_domain(self) -> VoucherEntity:
        return VoucherEntity(
            id=self.id,
            code=self.code,
            voucher_type=VoucherType(self.voucher_type),
            value=float(self.value),
            store_id=self.store_id,
            min_order_value=float(self.min_order_value),
            max_discount_amount=float(self.max_discount_amount) if self.max_discount_amount else None,
            usage_limit=self.usage_limit,
            usage_per_user=self.usage_per_user,
            start_date=self.start_date,
            end_date=self.end_date,
            is_active=self.is_active,
            current_usage=self.current_usage,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def __str__(self) -> str:
        return f"{self.code} ({self.store.name})"
