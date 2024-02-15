from rest_framework import serializers
from Purchases.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"


class PurchaseProductRequestSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    tax = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=9, decimal_places=2)
    product_id = serializers.IntegerField()


class PurchaseRequestSerializer(serializers.Serializer):
    reference_invoice = serializers.CharField(max_length=200)
    tax = serializers.DecimalField(max_digits=9, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=9, decimal_places=2)
    total = serializers.DecimalField(max_digits=9, decimal_places=2)
    provider = serializers.IntegerField()
    product = serializers.ListField(child=PurchaseProductRequestSerializer())
