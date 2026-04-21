from enum import Enum

class VoucherType(Enum):
    """Types of discount logic for vouchers."""
    
    FIXED = "FIXED"
    PERCENTAGE = "PERCENTAGE"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
