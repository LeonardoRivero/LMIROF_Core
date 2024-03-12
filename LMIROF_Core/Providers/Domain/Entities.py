from dataclasses import dataclass


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
    status: bool = True
    id: int = 0
    provider: int = 0
    sale_price: float = 0
    gain_business: float = 0
    gain_operational: float = 0
