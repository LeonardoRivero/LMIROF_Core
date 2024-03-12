import datetime
from dataclasses import dataclass, field
from typing import List


@dataclass
class SaledProductDTO:
    gain: float
    sale_price: float
    saled_to: float
    name: str
    quantity: int


@dataclass
class SummaryGainSellerDTO:
    date_sale: datetime.datetime
    reference_payment: str
    products: List[SaledProductDTO] = field(default_factory=list)
    sale_id: int = 0


@dataclass
class PaySellerDTO:
    name_seller: str
    total_to_pay: float = 0
    resume: List[SummaryGainSellerDTO] = field(default_factory=list)
