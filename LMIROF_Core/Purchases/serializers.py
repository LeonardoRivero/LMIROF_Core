from Purchases.models import Purchase
from rest_framework import serializers


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"
        depth = 0


class PurchaseProductRequestSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    product_id = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=9, decimal_places=2)


class PurchaseRequestSerializer(serializers.Serializer):
    reference_invoice = serializers.CharField(max_length=200)
    tax = serializers.DecimalField(max_digits=9, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=9, decimal_places=2)
    total = serializers.DecimalField(max_digits=9, decimal_places=2)
    provider = serializers.IntegerField()
    products = PurchaseProductRequestSerializer(many=True)
