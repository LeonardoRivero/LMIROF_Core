from rest_framework import serializers
from Providers.serializers import ProductSerializer
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Inventory
        fields = "__all__"
