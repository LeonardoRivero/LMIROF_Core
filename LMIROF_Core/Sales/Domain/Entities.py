from dataclasses import dataclass
from typing import Iterable, List
from Providers.Domain.Entities import ProductEntity
import datetime


@dataclass
class SellerEntity:
    name: str
    last_name: str
    identification_type: int
    identification: str
    address: str
    email: str = ""
    gender: int = 0
    status: bool = True
    id: int = 0


@dataclass
class SaleEntity:
    reference_payment: str
    date_created: datetime.datetime = None
    seller: int = 0
    id: int = 0


@dataclass
class SaleProductEntity:
    quantity: int = 0
    gain: int = 0
    sale_price: float = 0
    product: int = 0
    sale: int = 0
    total: float = 0
    id: int = 0
