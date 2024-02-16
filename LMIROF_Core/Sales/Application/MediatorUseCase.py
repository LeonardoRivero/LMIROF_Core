from Purchases.Application.PurchaseUseCases import GetPurchaseProductByFiltersUseCase
from Sales.Application.SellerUseCases import GetSellerByIdUseCase
from Sales.Domain.Entities import SellerEntity
from Sales.Application.SaleUseCases import GetSalesBySellerIdUseCase
from Providers.Application.ProductUseCases import GetProductByIdUseCase
from Sales.Domain.Interfaces import Mediator, UseCase
from django.db.models.query import QuerySet


class ConcreteMediator(Mediator):
    def __init__(self) -> None:
        self.getProductByUseCase = GetPurchaseProductByFiltersUseCase()
        self.getSalesBySellerIdUseCase = GetSalesBySellerIdUseCase()
        self.getSellerByIdUseCase = GetSellerByIdUseCase()

    def notify(self, sender: object, event: dict) -> object:
        if isinstance(sender, UseCase) and "product" in event.keys():
            r: QuerySet = self.getProductByUseCase.execute(event)
            return r.latest('id')
        if isinstance(sender, UseCase) and "seller_id" in event.keys():
            data = self.getSalesBySellerIdUseCase.execute(event["seller_id"])
            if data == None:
                return []
            return data

    def getSellerById(self, seller_id: int) -> SellerEntity:
        return self.getSellerByIdUseCase.execute(seller_id)
