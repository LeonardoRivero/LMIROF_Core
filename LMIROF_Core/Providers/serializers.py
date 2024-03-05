from rest_framework import serializers

from .models import Product, Provider


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ["id", "business_name", "identification_type",
                  "identification", "address", "country", "department", "city", "email", "status"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "provider",
                  "reference", "status", "distribution_type"]
        depth = 0
