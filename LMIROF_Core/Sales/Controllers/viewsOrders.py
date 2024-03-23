from http import HTTPStatus

from drf_spectacular.utils import extend_schema
from Inventory.Application.InventoryUseCases import DecrementProductBySaleUseCase
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from Sales.Domain.Request import OrderRequest

from LMIROF_Core.containers import container

from ..Application.MediatorUseCase import ConcreteMediator
from ..Application.OrderUseCase import CreateOrderUseCase, GetOrdersPendingUseCase
from ..Domain.Interfaces import UseCase


class CreateOrder(generics.CreateAPIView):
    serializer_class = container.order_serializer()
    use_case = CreateOrderUseCase(
        container.repositories("order"), container.repositories("order_product")
    )
    mediator = ConcreteMediator()
    decrement_product_use_case = DecrementProductBySaleUseCase(
        container.repositories("inventory")
    )

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = 1
        return self.serializer_class

    @extend_schema(
        request=container.order_product_request_serializer(),
        description="Create order",
        summary="Create a new order ",
    )
    def post(self, request: Request):
        try:
            entity = OrderRequest(**request.data)
            self.use_case.mediator = self.mediator
            data = self.use_case.execute(entity)
            self.decrement_product_use_case.execute(entity.products, data.id)
            response = self.get_serializer(data, many=False)
            return Response(response.data, HTTPStatus.CREATED)
        except TypeError as e:
            return Response(str(e), HTTPStatus.UNPROCESSABLE_ENTITY)
        except (ValueError, AssertionError) as e:
            return Response(str(e), HTTPStatus.BAD_REQUEST)


@extend_schema(
    description="List order",
    summary="List all orders ",
)
class ListOrders(generics.ListAPIView):
    queryset = container.model_order().objects.all()
    serializer_class = container.order_serializer()
    model = container.model_order()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = 1
        return self.serializer_class

    def get_queryset(self):
        return (
            container.model_order()
            .objects.select_related("seller")
            .prefetch_related("product")
            .defer("date_created", "last_modified")
        )


class GetOrdersPending(generics.RetrieveAPIView):
    serializer_class = container.order_serializer()
    use_case: UseCase = GetOrdersPendingUseCase(container.repositories("order"))
    mediator = ConcreteMediator()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = 1
        return self.serializer_class

    @extend_schema(
        description="Get all orders on state pending",
        summary="Get all orders on state pending",
    )
    def get(self, request: Request):
        try:
            self.use_case.mediator = self.mediator
            data = self.use_case.execute()
            response = self.get_serializer(data, many=True)
            return Response(response.data, HTTPStatus.OK)
        except (TypeError, ValueError):
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)
