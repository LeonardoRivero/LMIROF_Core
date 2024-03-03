from drf_spectacular.utils import extend_schema
from rest_framework import generics

from LMIROF_Core.containers import container


# Create your views here.


@extend_schema(
    description='Current state inventory',
    summary="Current state inventory ",
)
class ListAllProductsInventory(generics.ListAPIView):
    serializer_class = container.inventory_serializer()
    model = container.model_inventory()

    def get_queryset(self):
        return container.model_inventory().objects.select_related("product")
