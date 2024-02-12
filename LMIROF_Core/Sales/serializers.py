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


class ProductRequestSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    sale_price = serializers.DecimalField(max_digits=9, decimal_places=2)
    id = serializers.IntegerField()


class SaleRequestSerializer(serializers.Serializer):

    reference_payment = serializers.CharField(max_length=200)
    seller = serializers.IntegerField()
    product = serializers.ListField(child=ProductRequestSerializer())
