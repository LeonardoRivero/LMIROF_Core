from rest_framework import generics
from drf_spectacular.utils import extend_schema
from LMIROF_Core.containers import container
# Create your views here.


@extend_schema(
    description='Current state inventory',
    summary="Current state inventory ",
)
class ListAllProductsInventory(generics.ListAPIView):
    queryset = container.model_inventory().objects.all()
    serializer_class = container.inventory_serializer()
    model = container.model_inventory()
