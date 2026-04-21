import uuid
from typing import List, Optional
from apps.vouchers.domain.entities.voucher import VoucherEntity
from apps.vouchers.domain.repositories.voucher_repository import IVoucherRepository
from apps.vouchers.models import Voucher

class DjangoVoucherRepository(IVoucherRepository):
    """Django implementation of Voucher repository."""

    def save(self, voucher: VoucherEntity) -> None:
        defaults = {
            "code": voucher.code,
            "voucher_type": voucher.voucher_type.value,
            "value": voucher.value,
            "store_id": voucher.store_id,
            "min_order_value": voucher.min_order_value,
            "max_discount_amount": voucher.max_discount_amount,
            "usage_limit": voucher.usage_limit,
            "usage_per_user": voucher.usage_per_user,
            "current_usage": voucher.current_usage,
            "start_date": voucher.start_date,
            "end_date": voucher.end_date,
            "is_active": voucher.is_active,
        }
        Voucher.objects.update_or_create(id=voucher.id, defaults=defaults)

    def get_by_id(self, voucher_id: uuid.UUID) -> Optional[VoucherEntity]:
        try:
            model = Voucher.objects.get(id=voucher_id)
            return model.to_domain()
        except Voucher.DoesNotExist:
            return None

    def get_by_code(self, code: str, store_id: uuid.UUID) -> Optional[VoucherEntity]:
        try:
            model = Voucher.objects.get(code=code, store_id=store_id)
            return model.to_domain()
        except Voucher.DoesNotExist:
            return None

    def list_by_store(self, store_id: uuid.UUID) -> List[VoucherEntity]:
        queryset = Voucher.objects.filter(store_id=store_id)
        return [model.to_domain() for model in queryset]
