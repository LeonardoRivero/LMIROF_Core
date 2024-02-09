from django.shortcuts import render
from rest_framework import generics
from Settings.models import IDType
from Settings.serializers import IDTypeSerializer

# Create your views here.
class ListIDType (generics.ListAPIView):
    """
    Create an object Patient.
    """
    queryset = IDType.objects.all()
    serializer_class = IDTypeSerializer