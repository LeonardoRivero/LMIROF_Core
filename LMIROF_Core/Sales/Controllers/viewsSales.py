from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from Sales.Domain.Request import SaleRequest
from Sales.Application.SaleUseCases import CreateSaleUseCase
from http import HTTPStatus
from LMIROF_Core.containers import container


class CreateSale(generics.CreateAPIView):
    serializer_class = container.sale_serializer()
    use_case = CreateSaleUseCase()

    @extend_schema(
        request=container.sale_request_serializer(),
        description='Create sale',
        summary="Create a new sale ",
    )
    def post(self, request: Request):
        try:
            entity = SaleRequest(**request.data)
            data = self.use_case.execute(entity)
            response = self.serializer_class(data, many=False)
            return Response(response.data, HTTPStatus.CREATED)
        except (TypeError, ValueError) as e:
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)


@extend_schema(
    description='List sales',
    summary="List all sales ",
)
class ListSales(generics.ListAPIView):
    queryset = container.model_sale().objects.all()
    serializer_class = container.sale_serializer()
    model = container.model_sale()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class
