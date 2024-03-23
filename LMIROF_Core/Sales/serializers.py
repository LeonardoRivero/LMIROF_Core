from Providers.serializers import ProductSerializer
from rest_framework import serializers

from .models import Order, Sale, SaleProduct, Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            "id",
            "name",
            "last_name",
            "identification_type",
            "identification",
            "email",
            "address",
            "gender",
            "status",
        ]
        depth = 0


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            "id",
            "seller",
            "order",
            "reference_payment",
            "payment_method",
            "is_cash_payment",
            "is_finish",
            "gain_seller",
            "gain_business",
            "gain_operational",
            "total",
        ]
        depth = 0


class SaleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleProduct
        fields = [
            "quantity",
            "gain_seller",
            "gain_business",
            "sale_price",
            "product",
            "sale",
            "total",
        ]


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "seller", "product", "total"]
        depth = 0


# class ProductRequestSerializer(serializers.Serializer):
#     quantity = serializers.IntegerField()
#     sale_total = serializers.DecimalField(max_digits=9, decimal_places=2)
#     id = serializers.IntegerField()


class SaleRequestSerializer(serializers.Serializer):
    reference_payment = serializers.CharField(max_length=200)
    payment_method = serializers.IntegerField()
    is_cash_payment = serializers.BooleanField()
    order_id = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=9, decimal_places=2)


class SaledProductSerializer(serializers.Serializer):
    gain = serializers.CharField(max_length=200)
    sale_price = serializers.FloatField()
    saled_to = serializers.FloatField()
    name = serializers.CharField(max_length=200)
    quantity = serializers.IntegerField()


class OrderRequestSerializer(serializers.Serializer):
    class OrderProductRequestSerializer(serializers.Serializer):
        quantity = serializers.IntegerField()
        id = serializers.IntegerField()

    seller = serializers.IntegerField()
    products = OrderProductRequestSerializer(many=True)


class SummaryGainSellerSerializer(serializers.Serializer):
    date_sale = serializers.DateTimeField()
    reference_payment = serializers.CharField(max_length=200)
    products = SaledProductSerializer(many=True)
    sale_id = serializers.IntegerField()


class PaySellerSerializer(serializers.Serializer):
    name_seller = serializers.CharField(max_length=200)
    total_to_pay = serializers.FloatField()
    resume = serializers.ListField(child=SummaryGainSellerSerializer())
