from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List

from apps.vouchers.domain.value_objects.voucher_type import VoucherType

@dataclass
class VoucherEntity:
    """Core domain entity for Vouchers."""
    
    id: uuid.UUID
    code: str
    voucher_type: VoucherType
    value: float
    store_id: uuid.UUID
    
    # Limits
    min_order_value: float = 0.0
    max_discount_amount: Optional[float] = None
    usage_limit: int = 0  # 0 means unlimited
    usage_per_user: int = 1
    
    # Validity
    start_date: datetime = field(default_factory=datetime.now)
    end_date: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=180)) # 6 months
    
    # State
    is_active: bool = True
    current_usage: int = 0
    
    # Optional scope
    product_ids: List[uuid.UUID] = field(default_factory=list)
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_valid(self, order_value: float, user_usage_count: int = 0) -> bool:
        """Business logic to check if voucher can be applied."""
        if not self.is_active:
            return False
            
        now = datetime.now()
        if now < self.start_date or now > self.end_date:
            return False
            
        if self.usage_limit > 0 and self.current_usage >= self.usage_limit:
            return False
            
        if user_usage_count >= self.usage_per_user:
            return False
            
        if order_value < self.min_order_value:
            return False
            
        return True

    def calculate_discount(self, order_value: float) -> float:
        """Calculate the discount amount based on order value."""
        if self.voucher_type == VoucherType.FIXED:
            discount = self.value
        else: # PERCENTAGE
            discount = (order_value * self.value) / 100
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        
        return min(discount, order_value)
