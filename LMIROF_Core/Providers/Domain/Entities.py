from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ProviderEntity:
    business_name: str
    identification_type: int
    identification: str
    address: str
    country: int
    department: int
    city: int
    email: str = ""
    status: bool = True
    id: int = 0


@dataclass
class ProductEntity:
    name: str
    reference: str
    price: float = 0
    status: bool = True
    id: int = 0
    provider: int = 0
