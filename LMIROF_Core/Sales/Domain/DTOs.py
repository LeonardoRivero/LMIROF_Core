from dataclasses import dataclass, field
import datetime
from typing import List


@dataclass
class SaledProductDTO:
    gain: float
    sale_price: float
    name: str


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
