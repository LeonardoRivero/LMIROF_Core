import datetime
from dataclasses import dataclass, field
from typing import List


import dateutil.parser


@dataclass
class ProductRequest:
    quantity: int = 0
    sale_total: float = 0
    id: int = 0


@dataclass
class SaleRequest:
    reference_payment: str
    products: List[ProductRequest] = field(default_factory=list)
    seller: int = 0


@dataclass
class SummarySellerRequest:
    start: datetime.datetime = None
    end: datetime.datetime = None
    id: int = 0

    def __post_init__(self):
        start = dateutil.parser.parse(self.start)
        end = dateutil.parser.parse(self.end)
        if start.date() > end.date():
            raise ValueError('End date should be greater than start date')
