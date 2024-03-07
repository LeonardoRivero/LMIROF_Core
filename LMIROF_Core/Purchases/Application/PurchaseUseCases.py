from typing import Type

from django.db.models.query import QuerySet
from Purchases.Domain.Entities import PurchaseEntity, PurchaseProductEntity

from ..Domain.Interfaces import Repository, UseCase
from ..Domain.Request import PurchaseRequest


class CreatePurchaseUseCase(UseCase):

    def __init__(
        self,
        repository_purchase: Repository,
        repository_purchase_product: Repository,
    ):
        self.repository_purchase = repository_purchase
        self.repository_purchase_product = repository_purchase_product

    def execute(self, data: PurchaseRequest) -> PurchaseEntity:

        entity = PurchaseEntity(
            provider=data.provider,
            reference_invoice=data.reference_invoice,
            subtotal=data.subtotal,
            tax=int(data.tax),
            total=data.total,
        )
        record: PurchaseEntity = self.repository_purchase.add(entity)
        if record is None:
            raise TypeError()

        for item in data.products:
            quantity = item["quantity"]
            unit_price = item["unit_price"]
            total = ((float(unit_price)) * int(quantity)) * (
                1 + (int(data.tax) / 100)
            )
            purchase_product_entity = PurchaseProductEntity(
                quantity=int(quantity),
                total=round(total),
                purchase=record.id,
                product=item["product_id"],
                unit_price=unit_price,
            )
            self.repository_purchase_product.add(purchase_product_entity)
        return record


class GetPurchaseByIdUseCase(UseCase):
    def __init__(
        self, repository_purchase: Repository, repository_purchase_product: Repository
    ):
        self.repository_purchase = repository_purchase
        self.repository_purchase_product = repository_purchase_product

    def execute(self, id: int) -> PurchaseEntity:
        return self.repository_purchase.get_by_id(id)


class GetPurchaseProductByFiltersUseCase(UseCase):
    def __init__(
        self,
        repository_purchase: Type[Repository],
        repository_purchase_product: Type[Repository],
    ):
        self.repository_purchase = repository_purchase
        self.repository_purchase_product = repository_purchase_product

    def execute(self, filter: dict) -> QuerySet:
        return self.repository_purchase_product.find_by_parameter(filter)
