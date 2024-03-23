import datetime
from dataclasses import dataclass


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
    is_cash_payment: bool
    is_finish: bool
    id: int = 0
    seller: int = 0
    order: int = 0
    gain_seller: float = 0
    gain_business: float = 0
    gain_operational: float = 0
    total: float = 0
    payment_method: int = 0
    date_created: datetime.datetime = None
    last_modified: datetime.datetime = None


@dataclass
class SaleProductEntity:
    quantity: int = 0
    gain_seller: float = 0
    gain_business: float = 0
    gain_operational: float = 0
    sale_price: float = 0
    product: int = 0
    sale: int = 0
    total: float = 0
    id: int = 0


@dataclass
class OrderProductEntity:
    quantity: int = 0
    product: int = 0
    order: int = 0
    id: int = 0


@dataclass
class OrderEntity:
    seller: int = 0
    total: float = 0
    is_finish: bool = False
    id: int = 0
    date_created: datetime.datetime = None
    last_modified: datetime.datetime = None
