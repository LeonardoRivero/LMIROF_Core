from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from Inventory.Application.InventoryUseCases import DecrementProductBySaleUseCase
from Sales.Domain.Interfaces import Mediator
from Providers.Domain.Interfaces import UseCase
from Sales.Application.MediatorUseCase import ConcreteMediator
from Sales.Domain.DTOs import PaySellerDTO
from Sales.serializers import PaySellerSerializer
from Sales.Application.SellerUseCases import GetSummaryGainSellerUseCase
from Sales.Domain.Request import SaleRequest
from Sales.Application.SaleUseCases import CreateSaleUseCase, GetSalesBySellerIdUseCase
from http import HTTPStatus
from LMIROF_Core.containers import container


class CreateSale(generics.CreateAPIView):
    serializer_class = container.sale_serializer()
    mediator = ConcreteMediator()
    use_case = CreateSaleUseCase()
    decrement_product_use_case = DecrementProductBySaleUseCase()

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


@extend_schema(
    description='List sales with gain product',
    summary="List all sales with gain product ",
)
class ListSalesProduct(generics.ListAPIView):
    queryset = container.model_sale_product().objects.all()
    serializer_class = container.sale_product_serializer()
    model = container.model_sale_product()

    def get_serializer_class(self):
        self.serializer_class.Meta.depth = int(1)
        return self.serializer_class


class SearchByFilterSale(generics.RetrieveAPIView):
    serializer_class = container.sale_serializer()
    use_case = GetSalesBySellerIdUseCase()

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
            if (data == None):
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            is_many = True if len(data) > 1 else False
            response = self.get_serializer(data, many=is_many)
            return Response(response.data, HTTPStatus.CREATED)
        except (TypeError, ValueError) as e:
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)


class SummarySalesBySeller(generics.RetrieveAPIView):
    serializer_class = PaySellerSerializer()
    mediator: Mediator = ConcreteMediator()
    use_case: UseCase = GetSummaryGainSellerUseCase()

    @extend_schema(
        description='List sales by seller with resume',
        summary="List all sales by seller with resume",
    )
    def get(self, request: Request, seller_id: int = None):
        try:
            data = None
            if (seller_id == None):
                return Response(None, status=HTTPStatus.BAD_REQUEST)
            self.use_case.mediator = self.mediator
            data: PaySellerDTO = self.use_case.execute(seller_id)

            response = PaySellerSerializer(data, many=False)
            return Response(response.data, HTTPStatus.OK)
        except (TypeError, ValueError) as e:
            return Response(None, HTTPStatus.UNPROCESSABLE_ENTITY)
