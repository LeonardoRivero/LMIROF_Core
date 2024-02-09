from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from Sales.Domain.Entities import SellerEntity
from Sales.Application.SalesUseCases import CreateSellerUseCase
from http import HTTPStatus
from LMIROF_Core.containers import container

# Create your views here.


class CreateSeller(generics.CreateAPIView):
    serializer_class = container.seller_serializer()
    use_case = CreateSellerUseCase()

    @extend_schema(
        request=container.seller_serializer(),
        description='Create seller',
        summary="Create a new seller ",
    )
    def post(self, request: Request):
        try:
            entity = SellerEntity(**request.data)
            record = self.use_case.execute(entity)
            return Response(model_to_dict(record), HTTPStatus.CREATED)
        except TypeError as e:
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)


@extend_schema(
    request=container.seller_serializer(),
    description='List sellers',
    summary="List all sellers ",
)
class ListSeller(generics.ListAPIView):
    queryset = container.model_seller().objects.all()
    serializer_class = container.seller_serializer()
    model = container.model_seller()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class
