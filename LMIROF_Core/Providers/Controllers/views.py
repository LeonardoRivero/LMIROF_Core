from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from Providers.Domain.Entities import ProductEntity, ProviderEntity
from Providers.Application.ProviderUseCases import CreateProductUseCase, CreateProviderUseCase, GetProductByNameUseCase
from Providers.serializers import ProviderSerializer
from http import HTTPStatus
from LMIROF_Core.containers import container
# Create your views here.


class CreateProvider(generics.CreateAPIView):
    serializer_class = container.provider_serializer()
    use_case = CreateProviderUseCase()

    @extend_schema(
        request=ProviderSerializer,
        description='Create provider',
        summary="Create a new provider ",
    )
    def post(self, request: Request):
        try:
            entity = ProviderEntity(**request.data)
            record = self.use_case.execute(entity)
            return Response(model_to_dict(record), HTTPStatus.CREATED)
        except TypeError as e:
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)


@extend_schema(
    request=ProviderSerializer,
    description='List provider',
    summary="List all provider ",
)
class ListProviders(generics.ListAPIView):
    queryset = container.model_provider().objects.all()
    serializer_class = container.provider_serializer()
    model = container.model_provider()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class


class CreateProduct(generics.CreateAPIView):
    serializer_class = container.product_serializer()
    use_case = CreateProductUseCase()

    @extend_schema(
        request=container.product_serializer(),
        description='Create product',
        summary="Create a new product ",
    )
    def post(self, request: Request):
        try:
            entity = ProductEntity(**request.data)
            record = self.use_case.execute(entity)
            return Response(model_to_dict(record), HTTPStatus.CREATED)
        except TypeError as e:
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)


@extend_schema(
    request=ProviderSerializer,
    description='List product',
    summary="List all product ",
)
class ListProduct(generics.ListAPIView):
    queryset = container.model_product().objects.all()
    serializer_class = container.product_serializer()
    model = container.model_product()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class


class FilterProduct(generics.RetrieveAPIView):
    serializer_class = container.product_serializer()
    use_case = GetProductByNameUseCase()

    @extend_schema(
        responses=container.product_serializer(),
        parameters=[
            OpenApiParameter(name='name', description='Name',
                             type=str, required=False)
        ]
    )
    def get(self, request: Request, pk: int = None) -> Response:
        try:
            data = None
            if ("name" in request.query_params):
                data = self.use_case.execute(
                    request.query_params["name"])
            if (data == None):
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            response = self.serializer_class(data, many=True)
            return Response(response.data, status=HTTPStatus.ACCEPTED)
        except KeyError as e:
            return Response(str(e), status=HTTPStatus.UNPROCESSABLE_ENTITY, exception=True)
