from dataclasses import dataclass


@dataclass
class ProviderEntity:
    business_name: str
    identification_type: int
    identification: str
    address: str
    country: int
    department: int
    city: int
    email: str = ""
    status: bool = True
    id: int = 0


@dataclass
class ProductEntity:
    name: str
    reference: str
    status: bool = True
    id: int = 0
    provider: int = 0
    sale_price:float=0
    profit_seller : float=0
    profit_bussiness : float=0
    profit_operational : float=0
    
    def __post_init__(self):
        sum_profits=self.profit_seller+self.profit_operational+self.profit_bussiness
        if sum_profits>1:
            raise ValueError("hp bruto no puede superar la unidad")

