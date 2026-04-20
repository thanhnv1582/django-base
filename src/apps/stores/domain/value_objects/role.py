from enum import Enum

class StoreRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    STAFF = "staff"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
