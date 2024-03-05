from rest_framework import generics
from Settings.models import DistributionProductType, IDType
from Settings.serializers import DistributionProductTypeSerializer, IDTypeSerializer

# Create your views here.


class ListIDType (generics.ListAPIView):
    """
    Create an object Id Types.
    """
    queryset = IDType.objects.all()
    serializer_class = IDTypeSerializer


class ListDistributionProductType (generics.ListAPIView):
    """
    Create an object all distributio products type.
    """
    queryset = DistributionProductType.objects.all()
    serializer_class = DistributionProductTypeSerializer
