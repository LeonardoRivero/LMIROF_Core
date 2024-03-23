from django.db.models.query import QuerySet
from Providers.Application.ProductUseCases import GetProductByIdUseCase
from Providers.Domain.Entities import ProductEntity
from Purchases.Application.PurchaseUseCases import GetPurchaseProductByFiltersUseCase
from Sales.Application.OrderUseCase import ToFinishOrderUseCase
from Sales.Application.SaleUseCases import (
    GetAllSalesPendingUseCase,
    GetSalesBySellerIdUseCase,
)
from Sales.Application.SellerUseCases import GetSellerByIdUseCase
from Sales.Domain.Entities import SellerEntity
from Sales.Domain.Interfaces import Mediator, UseCase
from Sales.Domain.Request import SummarySellerRequest

from LMIROF_Core.containers import container


class ConcreteMediator(Mediator):
    def __init__(self) -> None:
        self.getPurchaseProductByFiltersUseCase = GetPurchaseProductByFiltersUseCase(
            container.repositories("purchase"),
            container.repositories("purchase_product"),
        )
        self.getSalesBySellerIdUseCase = GetSalesBySellerIdUseCase(
            container.repositories("sale")
        )
        self.getSellerByIdUseCase = GetSellerByIdUseCase(
            container.repositories("seller")
        )
        self.getProductbyIdUseCase = GetProductByIdUseCase(
            container.repositories("product")
        )
        self.getAllSalesPendingUseCase = GetAllSalesPendingUseCase(
            container.repositories("sale")
        )
        self.toFinishOrderUseCase = ToFinishOrderUseCase(
            container.repositories("order")
        )

    def notify(self, sender: object, event: dict) -> object:
        if isinstance(sender, UseCase) and "product" in event.keys():
            queryset: QuerySet = self.getPurchaseProductByFiltersUseCase.execute(event)
            return queryset.latest("id")
        # if isinstance(sender, UseCase) and "seller_id" in event.keys():
        #     data = self.getSalesBySellerIdUseCase.execute(event["seller_id"])
        #     if data == None:
        #         return []
        #     return data

    def getSellerById(self, seller_id: int) -> SellerEntity:
        return self.getSellerByIdUseCase.execute(seller_id)

    def getProductById(self, product_id: int) -> ProductEntity:
        return self.getProductbyIdUseCase.execute(product_id)

    def getResumeSalesSeller(self, request: SummarySellerRequest):
        data = self.getSalesBySellerIdUseCase.execute(request)
        if data is None:
            return []
        return data

    def getAllOrdersPending(self) -> QuerySet:
        return self.getAllSalesPendingUseCase.execute()

    def toFinishOrder(self, id_order: int) -> SellerEntity:
        return self.toFinishOrderUseCase.execute(id_order)
