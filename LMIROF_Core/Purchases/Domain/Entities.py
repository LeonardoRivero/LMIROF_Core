from dataclasses import dataclass


@dataclass
class PurchaseEntity:
    reference_invoice: str
    subtotal: float = 0
    tax: int = 0
    total: float = 0
    provider: int = 0
    id: int = 0


@dataclass
class PurchaseProductEntity:
    total: float = 0
    unit_price: float = 0
    quantity: int = 0
    purchase: int = 0
    product: int = 0
    id: int = 0
