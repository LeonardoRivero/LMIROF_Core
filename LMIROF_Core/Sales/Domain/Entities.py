from dataclasses import dataclass
from typing import Iterable,List
from Providers.Domain.Entities import ProductEntity


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
class PurchaseEntity:
    invoice_id:str
    provider: int = 0
    id: int = 0

@dataclass
class SaleEntity:
    reference_payment:str
    seller: int = 0
    id: int = 0

@dataclass
class SaleProductEntity:
    total:float=0
    sale:int=0
    product:int=0
    sale_price:float=0
    gain:float=0
    quantity: int = 0
    id: int = 0