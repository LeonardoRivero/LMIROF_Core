from typing import List, Type

from django.db.models import QuerySet,Model

from Purchases.Domain.Request import ProductPurchaseRequest
from Sales.Domain.Request import ProductRequest

from ..Domain.Entities import InventoryEntity
from ..Domain.Interfaces import Repository, UseCase


class IncrementProductByPurchaseUseCase(UseCase):
    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(self, list_products: List[ProductPurchaseRequest], purchase_id: int) -> List[InventoryEntity]:
        for product in list_products:
            product_registered = self.repository.find_by_parameter(
                {"product": product["product_id"]})

            if (product_registered is not None):
                entity: InventoryEntity = self.repository.get_by_id(
                    product["product_id"])
                input_total = entity.input + int(product["quantity"])
                stock = entity.stock + int(product["quantity"])
                entity_updated = InventoryEntity(product=product["product_id"],
                                                 input=input_total,
                                                 output=entity.output,
                                                 stock=stock,
                                                 operation_type="PURCHASE",
                                                 operation_id=purchase_id
                                                 )

                self.repository.update(entity_updated,  product["product_id"])
            else:
                new_entity = InventoryEntity(
                    product=product["product_id"],
                    input=int(product["quantity"]),
                    output=0,
                    stock=int(product["quantity"]),
                    operation_type="PURCHASE",
                    operation_id=purchase_id)
                self.repository.add(new_entity)


class DecrementProductBySaleUseCase(UseCase):
    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(self, list_products: List[ProductRequest], sale_id: int) -> List[InventoryEntity]:
        try:
            for product in list_products:
                entity: InventoryEntity = self.repository.get_by_id(
                    product["id"])
                output_total = entity.output + int(product["quantity"])
                stock = entity.stock - int(product["quantity"])
                entity_updated = InventoryEntity(stock=stock,
                                                 input=entity.input,
                                                 output=output_total,
                                                 operation_type="SALE",
                                                 product=product["id"],
                                                 operation_id=sale_id)

                self.repository.update(entity_updated,  product["id"])
        except Exception:
            new_entity = InventoryEntity(
                operation_type="SALE", carrying_amount=int(product["quantity"])*float(product["sale_price"]), available_quantity=int(product["quantity"]), product=product["id"])
            self.repository.add(new_entity)


class GetStockByProductIdUseCase(UseCase):
    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(self, product_id: str) -> Type[Model]:
        record: Model = self.repository.get_by_id(product_id)
        return record
