from rest_framework import serializers
from .models import Purchase, Sale, Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"