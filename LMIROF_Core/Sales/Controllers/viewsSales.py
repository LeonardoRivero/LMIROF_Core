import datetime
from http import HTTPStatus

from drf_spectacular.utils import OpenApiParameter, extend_schema
from Inventory.Application.InventoryUseCases import DecrementProductBySaleUseCase
from Providers.Domain.Interfaces import UseCase
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from Sales.Application.MediatorUseCase import ConcreteMediator
from Sales.Application.SaleUseCases import (
    CreateSaleUseCase,
    GetSaleByIdUseCase,
    GetSaleByReference,
    GetSalesBySellerIdUseCase,
)
from Sales.Application.SellerUseCases import GetSummaryGainSellerUseCase
from Sales.Domain.DTOs import PaySellerDTO
from Sales.Domain.Interfaces import Mediator
from Sales.Domain.Request import SaleRequest, SummarySellerRequest
from Sales.serializers import PaySellerSerializer

from LMIROF_Core.containers import container


class CreateSale(generics.CreateAPIView):
    serializer_class = container.sale_serializer()
    mediator = ConcreteMediator()
    use_case = CreateSaleUseCase(container.repositories(
        "sale"), container.repositories("sale_product"))
    decrement_product_use_case = DecrementProductBySaleUseCase(
        container.repositories("inventory"))

    @extend_schema(
        request=container.sale_request_serializer(),
        description='Create sale',
        summary="Create a new sale ",
    )
    def post(self, request: Request):
        try:
            entity = SaleRequest(**request.data)
            self.use_case.mediator = self.mediator
            data = self.use_case.execute(entity)
            self.decrement_product_use_case.execute(entity.products, data.id)
            response = self.serializer_class(data, many=False)
            return Response(response.data, HTTPStatus.CREATED)
        except (TypeError, ValueError) as e:
            return Response(str(e), HTTPStatus.UNPROCESSABLE_ENTITY)


@extend_schema(
    description='List sales',
    summary="List all sales ",
)
class ListSales(generics.ListAPIView):
    queryset = container.model_sale().objects.all()
    serializer_class = container.sale_serializer()
    model = container.model_sale()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = 1
        return self.serializer_class

    def get_queryset(self):
        return container.model_sale().objects.select_related("seller").prefetch_related("product").defer("date_created", "last_modified")


@extend_schema(
    description='List sales with gain product',
    summary="List all sales with gain product ",
)
class ListSalesProduct(generics.ListAPIView):
    serializer_class = container.sale_product_serializer()
    model = container.model_sale_product()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = 1
        return self.serializer_class

    def get_queryset(self):
        return container.model_sale_product().objects.select_related("sale", "product").all()


class SearchByFilterSale(generics.RetrieveAPIView):
    serializer_class = container.sale_serializer()
    use_case = GetSalesBySellerIdUseCase(container.repositories("seller"))

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class

    @extend_schema(
        description='List sales by seller on current month',
        summary="List all sales by seller on current month",
        parameters=[
            OpenApiParameter(name='id_seller', description='id_seller',
                             type=str, required=False)
        ]
    )
    def get(self, request: Request):
        try:
            data = None
            if ("id_seller" in request.query_params):
                data = self.use_case.execute(
                    int(request.query_params["id_seller"]))
            if (data is None):
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            is_many = True if len(data) > 1 else False
            response = self.get_serializer(data, many=is_many)
            return Response(response.data, HTTPStatus.CREATED)
        except (TypeError, ValueError):
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)


class SummarySalesBySeller(generics.RetrieveAPIView):
    serializer_class = container.payseller_serializer
    mediator: Mediator = ConcreteMediator()
    use_case: UseCase = GetSummaryGainSellerUseCase(
        container.repositories("sale"), container.repositories("sale_product"))

    @extend_schema(
        description='List sales by seller with resume',
        summary="List all sales by seller with resume",
        parameters=[
            OpenApiParameter(name='start', description='start_date',
                             type=datetime.datetime, required=False, default=datetime.datetime.today()),
            OpenApiParameter(name='end', description='end',
                             type=datetime.datetime, required=False, default=datetime.datetime.today()+datetime.timedelta(7))
        ]
    )
    def get(self, request: Request, seller_id: int = None):
        try:
            data = None
            if (seller_id is None or "start" not in request.query_params or "end" not in request.query_params):
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            payload = SummarySellerRequest(
                id=seller_id,
                start=request.query_params["start"],
                end=request.query_params["end"])
            self.use_case.mediator = self.mediator
            data: PaySellerDTO = self.use_case.execute(payload)

            response = PaySellerSerializer(data, many=False)
            return Response(response.data, HTTPStatus.OK)
        except (TypeError, ValueError) as e:
            return Response(e.args, HTTPStatus.UNPROCESSABLE_ENTITY)


class GetSaleByID(generics.RetrieveAPIView):
    serializer_class = container.sale_serializer()
    use_case: UseCase = GetSaleByIdUseCase(container.repositories("sale"))

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class

    @extend_schema(
        description='Get Sale by ID',
        summary="Get Sale by ID",
    )
    def get(self, request: Request, sale_id: int = None):
        try:
            data = None
            if (sale_id is None):
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            data = self.use_case.execute(sale_id)
            if (data is None):
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            response = self.get_serializer(data, many=False)
            return Response(response.data, HTTPStatus.OK)
        except (TypeError, ValueError):
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)


class FilterSale(generics.RetrieveAPIView):
    serializer_class = container.sale_serializer()
    use_case = GetSaleByReference(container.repositories("sale"))

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class

    @extend_schema(
        responses=container.product_serializer(),
        parameters=[
            OpenApiParameter(name='reference', description='reference_sale',
                             type=str, required=False)
        ]
    )
    def get(self, request: Request, pk: int = None) -> Response:
        try:
            data = None
            if ("reference" in request.query_params):
                data = self.use_case.execute(
                    request.query_params["reference"])
            if (data is None):
                return Response(None, status=HTTPStatus.NO_CONTENT)
            response = self.get_serializer(data, many=True)
            return Response(response.data, status=HTTPStatus.ACCEPTED)
        except KeyError as e:
            return Response(str(e), status=HTTPStatus.UNPROCESSABLE_ENTITY, exception=True)
