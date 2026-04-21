import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from apps.vouchers.domain.entities.voucher import VoucherEntity
from apps.vouchers.domain.value_objects.voucher_type import VoucherType
from apps.vouchers.domain.repositories.voucher_repository import IVoucherRepository

@dataclass
class CreateVoucherDTO:
    code: str
    voucher_type: str
    value: float
    store_id: str
    min_order_value: float = 0.0
    max_discount_amount: Optional[float] = None
    usage_limit: int = 0
    usage_per_user: int = 1
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CreateVoucherUseCase:
    def __init__(self, voucher_repo: IVoucherRepository):
        self.voucher_repo = voucher_repo

    def execute(self, dto: CreateVoucherDTO) -> VoucherEntity:
        # Business Rule: Default dates if not provided
        start_date = dto.start_date or datetime.now()
        end_date = dto.end_date or (start_date + timedelta(days=180)) # Default 6 months

        voucher = VoucherEntity(
            id=uuid.uuid4(),
            code=dto.code,
            voucher_type=VoucherType(dto.voucher_type),
            value=dto.value,
            store_id=uuid.UUID(dto.store_id),
            min_order_value=dto.min_order_value,
            max_discount_amount=dto.max_discount_amount,
            usage_limit=dto.usage_limit,
            usage_per_user=dto.usage_per_user,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )

        # In a real scenario, we would check if code already exists for this store
        self.voucher_repo.save(voucher)
        return voucher
