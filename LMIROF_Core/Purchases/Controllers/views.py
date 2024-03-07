from http import HTTPStatus

from drf_spectacular.utils import extend_schema
from Inventory.Application.InventoryUseCases import IncrementProductByPurchaseUseCase
from Purchases.Application.PurchaseUseCases import (
    CreatePurchaseUseCase,
    GetPurchaseByIdUseCase,
)
from Purchases.Domain.Interfaces import UseCase
from Purchases.Domain.Request import PurchaseRequest
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from LMIROF_Core.containers import container


class CreatePurchase(generics.CreateAPIView):
    serializer_class = container.purchase_serializer()
    use_case = CreatePurchaseUseCase(
        container.repositories(
            "purchase"), container.repositories("purchase_product")
    )
    increment_product_use_case = IncrementProductByPurchaseUseCase(
        container.repositories("inventory"),
    )

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class

    @extend_schema(
        request=container.purchase_request_serializer(),
        description="Create purchase to provider",
        summary="Create a purchase to provider ",
    )
    def post(self, request: Request):
        try:
            data = PurchaseRequest(**request.data)
            record = self.use_case.execute(data)
            response = self.get_serializer(record, many=False)
            self.increment_product_use_case.execute(data.products, record.id)
            return Response(response.data, HTTPStatus.CREATED)
        except TypeError:
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)


class GetPurchaseByID(generics.RetrieveAPIView):
    serializer_class = container.purchase_serializer()
    use_case: UseCase = GetPurchaseByIdUseCase(
        container.repositories(
            "purchase"), container.repositories("purchase_product")
    )

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class

    @extend_schema(
        description="Get Purchase by ID",
        summary="Get Purchase by ID",
    )
    def get(self, request: Request, purchase_id: int | None = None):
        try:
            data = None
            if purchase_id is None:
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            data = self.use_case.execute(purchase_id)
            if data is None:
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            response = self.get_serializer(data, many=False)
            return Response(response.data, HTTPStatus.OK)
        except (TypeError, ValueError):
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)


# @extend_schema(
#     description='List purchases',
#     summary="List all purchases ",
# )
# class ListPurchases(generics.ListAPIView):
#     queryset = container.model_purchase().objects.all()
#     serializer_class = container.purchase_serializer()
#     model = container.model_purchase()

#     def get_serializer_class(self):
#         self.serializer_class.Meta.depth = int(1)
#         return self.serializer_class
#     model = container.model_purchase()

#     def get_serializer_class(self):
#         self.serializer_class.Meta.depth = int(1)
#         return self.serializer_class
