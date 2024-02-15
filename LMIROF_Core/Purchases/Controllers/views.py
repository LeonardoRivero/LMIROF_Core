from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from Purchases.Domain.Interfaces import UseCase
from Purchases.Application.PurchaseUseCases import CreatePurchaseUseCase, GetPurchaseByIdUseCase
from Purchases.Domain.Request import PurchaseRequest
from http import HTTPStatus
from LMIROF_Core.containers import container


class CreatePurchase(generics.CreateAPIView):
    serializer_class = container.purchase_serializer()
    use_case = CreatePurchaseUseCase()

    @extend_schema(
        request=container.purchase_request_serializer(),
        description='Create purchase to provider',
        summary="Create a purchase to provider ",
    )
    def post(self, request: Request):
        try:
            data = PurchaseRequest(**request.data)
            record = self.use_case.execute(data)
            response = self.serializer_class(record, many=False)
            return Response(response.data, HTTPStatus.CREATED)
        except TypeError as e:
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)


class GetPurchaseByID(generics.RetrieveAPIView):
    serializer_class = container.purchase_serializer()
    use_case: UseCase = GetPurchaseByIdUseCase()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class

    @extend_schema(
        description='Get Purchase by ID',
        summary="Get Purchase by ID",
    )
    def get(self, request: Request, purchase_id: int = None):
        try:
            data = None
            if (purchase_id == None):
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            data = self.use_case.execute(purchase_id)
            if (data == None):
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            response = self.get_serializer(data, many=False)
            return Response(response.data, HTTPStatus.OK)
        except (TypeError, ValueError) as e:
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)
