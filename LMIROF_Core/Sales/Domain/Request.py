from dataclasses import dataclass, field
from typing import Iterable, List
from Providers.Domain.Entities import ProductEntity
from Sales.Domain.Entities import PurchaseEntity, SaleEntity


@dataclass
class ProductRequest:
    quantity: int = 0
    sale_price: float = 0
    product: int = 0
    id: int = 0


@dataclass
class SaleRequest:
    reference_payment: str
    product: List[ProductRequest] = field(default_factory=list)
    seller: int = 0
