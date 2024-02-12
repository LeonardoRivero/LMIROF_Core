from Providers.Application.ProductUseCases import GetProductByIdUseCase
from Sales.Domain.Interfaces import Mediator, UseCase


class ConcreteMediator(Mediator):
    def __init__(self) -> None:
        self.getProductByUseCase = GetProductByIdUseCase()

    def notify(self, sender: UseCase, event: dict) -> None:
        if isinstance(sender, UseCase) and "product_id" in event.keys():
            return self.getProductByUseCase.execute(event["product_id"])
