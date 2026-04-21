import uuid
from typing import List
from apps.vouchers.domain.entities.voucher import VoucherEntity
from apps.vouchers.domain.repositories.voucher_repository import IVoucherRepository

class ListVouchersUseCase:
    def __init__(self, voucher_repo: IVoucherRepository):
        self.voucher_repo = voucher_repo

    def execute(self, store_id: str) -> List[VoucherEntity]:
        return self.voucher_repo.list_by_store(uuid.UUID(store_id))
