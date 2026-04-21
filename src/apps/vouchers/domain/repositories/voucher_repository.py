import uuid
from abc import ABC, abstractmethod
from typing import List, Optional
from apps.vouchers.domain.entities.voucher import VoucherEntity

class IVoucherRepository(ABC):
    """Interface for Voucher persistence."""
    
    @abstractmethod
    def save(self, voucher: VoucherEntity) -> None:
        """Persist a voucher."""
        pass

    @abstractmethod
    def get_by_id(self, voucher_id: uuid.UUID) -> Optional[VoucherEntity]:
        """Retrieve a voucher by ID."""
        pass

    @abstractmethod
    def get_by_code(self, code: str, store_id: uuid.UUID) -> Optional[VoucherEntity]:
        """Retrieve a voucher by code for a specific store."""
        pass

    @abstractmethod
    def list_by_store(self, store_id: uuid.UUID) -> List[VoucherEntity]:
        """List all vouchers for a store."""
        pass
