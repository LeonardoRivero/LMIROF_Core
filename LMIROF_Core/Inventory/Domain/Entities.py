from dataclasses import dataclass


@dataclass
class OperationTypeEntity:
    description: str = 0
    id: int = 0


@dataclass
class InventoryEntity:
    product: int
    input: int
    output: int
    stock: int
    operation_type: int
    operation_id: int
    # carrying_amount: float = 0
