import datetime
from typing import List

from ..Domain.Entities import OrderEntity, OrderProductEntity
from ..Domain.Interfaces import Repository, UseCase
from ..Domain.Request import OrderRequest


class CreateOrderUseCase(UseCase):
    def __init__(
        self, repository_order: Repository, repository_order_product: Repository
    ):
        self.repository_order = repository_order
        self.repository_order_product = repository_order_product

    def execute(self, request: OrderRequest) -> OrderEntity:
        dict_products = {}
        total = 0
        for item in request.products:
            response = self.mediator.getProductById(item["id"])
            total = total + (response.sale_price * item["quantity"])
            dict_products.update({response.id: response})

        list_order_product: List[OrderProductEntity] = []

        for item in request.products:
            order_product = OrderProductEntity(
                product=item["id"], quantity=item["quantity"], order=0
            )
            list_order_product.append(order_product)

        order = OrderEntity(total=total, seller=request.seller, is_finish=False)
        record = self.repository_order.add(order)

        for order_products in list_order_product:
            order_products.order = record.id
            self.repository_order_product.add(order_products)
        return record


class GetOrdersPendingUseCase(UseCase):
    def __init__(self, repository_order: Repository):
        self.repository_order = repository_order

    def execute(self) -> OrderEntity:
        # queryset = self.mediator.getAllOrdersPending()
        # list_test: List[OrderEntity] = []
        # t = queryset.values_list("order_id", flat=True).distinct()

        # for a in t:
        #     h = self.repository_order.get_by_id(a)
        #     list_test.append(h)
        # return list_test
        return self.repository_order.find_by_parameter({"is_finish": False})


class ToFinishOrderUseCase(UseCase):
    def __init__(self, repository_order: Repository):
        self.repository_order = repository_order

    def execute(self, order_id: int) -> OrderEntity:
        model = self.repository_order.get_by_id(order_id)
        entity = OrderEntity(
            id=order_id,
            is_finish=True,
            seller=model.seller_id,
            total=model.total,
            last_modified=datetime.datetime.today(),
        )
        return self.repository_order.update(entity, order_id)
