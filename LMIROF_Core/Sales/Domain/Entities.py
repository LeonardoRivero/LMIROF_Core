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
