from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from Sales.Domain.Request import PurchaseRequest
from Sales.Application.SaleUseCases import CreateSaleUseCase
from http import HTTPStatus
from LMIROF_Core.containers import container

class CreateSale(generics.CreateAPIView):
    serializer_class = container.sale_serializer()
    use_case = CreateSaleUseCase()

    @extend_schema(
        request=container.seller_serializer(),
        description='Create sale',
        summary="Create a new sale ",
    )
    def post(self, request: Request):
        try:
            entity = PurchaseRequest(**request.data)
            record = self.use_case.execute(entity)
            return Response(model_to_dict(record), HTTPStatus.CREATED)
        except TypeError as e:
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)