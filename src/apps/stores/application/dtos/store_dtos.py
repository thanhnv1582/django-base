from dataclasses import dataclass
from typing import Optional, List
import uuid

@dataclass
class StoreCreateDTO:
    name: str
    description: str = ""
    address: str = ""
    phone: str = ""
    logo: Optional[str] = None

@dataclass
class StoreReadDTO:
    id: uuid.UUID
    name: str
    slug: str
    description: str
    address: str
    phone: str
    logo: Optional[str]
    is_active: bool
    created_at: str

@dataclass
class StoreMemberReadDTO:
    user_id: uuid.UUID
    role: str
