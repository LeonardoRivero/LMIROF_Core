from dataclasses import dataclass
from typing import Iterable,List
from Providers.Domain.Entities import ProductEntity
from Sales.Domain.Entities import PurchaseEntity


@dataclass
class PurchaseRequest(PurchaseEntity):
    product: List[ProductEntity]=[]
