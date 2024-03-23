import datetime
from dataclasses import dataclass, field
from typing import List

import dateutil.parser


class ProductRequest:
    quantity: int = 0
    sale_total: float = 0
    id: int = 0


@dataclass
class SaleRequest:
    reference_payment: str
    order_id: int = 0
    payment_method: int = 0
    is_cash_payment: bool = True
    total: float = 0


@dataclass
class SummarySellerRequest:
    start: datetime.datetime = None
    end: datetime.datetime = None
    id: int = 0

    def __post_init__(self):
        start = dateutil.parser.parse(self.start)
        end = dateutil.parser.parse(self.end)
        if start.date() > end.date():
            raise ValueError("End date should be greater than start date")


class OrderProduct:
    quantity: int = 0
    id: int = 0


@dataclass
class OrderRequest:
    products: List[OrderProduct] = field(default_factory=list)
    seller: int = 0

    def __post_init__(self):
        for product in self.products:
            assert product["quantity"] != 0, "Quantity cant be zero"
