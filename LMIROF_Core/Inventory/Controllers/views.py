from drf_spectacular.utils import extend_schema
from rest_framework import generics
from drf_spectacular.utils import OpenApiParameter, extend_schema
from ..Application.InventoryUseCases import GetStockByProductIdUseCase

from LMIROF_Core.containers import container
from rest_framework.request import Request
from rest_framework.response import Response

from http import HTTPStatus
# Create your views here.


@extend_schema(
    description='Current state inventory',
    summary="Current state inventory ",
)
class ListAllProductsInventory(generics.ListAPIView):
    serializer_class = container.inventory_serializer()
    model = container.model_inventory()

    def get_queryset(self):
        return container.model_inventory().objects.select_related("product").all()

class GetStockByProductId(generics.RetrieveAPIView):
    serializer_class = container.inventory_serializer()
    use_case = GetStockByProductIdUseCase(container.repositories("inventory"))

    @extend_schema(
        responses=container.inventory_serializer(),
        description='Get stock by id product',
        summary="Get stock by id product",
    )
    def get(self, request: Request, product_id: int | None = None) -> Response:
        try:
            data = self.use_case.execute(product_id)
            response = self.serializer_class(data, many=False)
            return Response(response.data, status=HTTPStatus.ACCEPTED)
        except KeyError as e:
            return Response(
                str(e), status=HTTPStatus.UNPROCESSABLE_ENTITY, exception=True
            )