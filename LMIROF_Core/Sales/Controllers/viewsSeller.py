from http import HTTPStatus

from django.forms import model_to_dict
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from Sales.Application.SellerUseCases import CreateSellerUseCase
from Sales.Domain.Entities import SellerEntity

from LMIROF_Core.containers import container

# Create your views here.
# Actuaizar catalogo
# Reuniones cada 15 dias
# Genrerar froamto para reportes


class CreateSeller(generics.CreateAPIView):
    serializer_class = container.seller_serializer()
    use_case = CreateSellerUseCase(container.repositories("seller"))

    @extend_schema(
        request=container.seller_serializer(),
        description="Create seller",
        summary="Create a new seller ",
    )
    def post(self, request: Request):
        try:
            entity = SellerEntity(**request.data)
            record = self.use_case.execute(entity)
            return Response(model_to_dict(record), HTTPStatus.CREATED)
        except TypeError as e:
            return Response(str(e), HTTPStatus.UNPROCESSABLE_ENTITY)


@extend_schema(
    request=container.seller_serializer(),
    description="List sellers",
    summary="List all sellers ",
)
class ListSeller(generics.ListAPIView):
    serializer_class = container.seller_serializer()
    model = container.model_seller()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class

    def get_queryset(self):
        return (
            container.model_seller()
            .objects.select_related("gender", "identification_type")
            .defer("date_created", "last_modified")
            .filter(status=True)
        )
