from dataclasses import dataclass, field
from typing import List


@dataclass
class ProductPurchaseRequest:
    tax: float = 0
    unit_price: float = 0
    quantity: int = 0
    product_id: int = 0


@dataclass
class PurchaseRequest:
    reference_invoice: str
    tax: float = 0
    subtotal: float = 0
    total: float = 0
    provider: int = 0
    products: List[ProductPurchaseRequest] = field(default_factory=list)
