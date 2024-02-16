from Inventory.Domain.Entities import InventoryEntity
from Inventory.Domain.Interfaces import Mediator
from Inventory.Application.InventoryUseCases import IncrementProductByPurchaseUseCase


class ConcreteMediator(Mediator):
    def __init__(self) -> None:
        self.incrementProductByPurchaseUseCase = IncrementProductByPurchaseUseCase()

    def addProductToInventory(self, entity: InventoryEntity):
        return self.incrementProductByPurchaseUseCase.execute(entity)
