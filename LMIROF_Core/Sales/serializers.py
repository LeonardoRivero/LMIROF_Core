from rest_framework import serializers

from .models import Sale, SaleProduct, Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["id", "name", "last_name", "identification_type",
                  "identification", "email", "address", "gender", "status"]


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ["id", "seller", "product", "reference_payment"]
        depth = 0


class SaleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleProduct
        fields = ["quantity", "gain_seller",
                  "gain_business", "sale_price", "product", "sale", "total"]


class ProductRequestSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    sale_total = serializers.DecimalField(max_digits=9, decimal_places=2)
    id = serializers.IntegerField()


class SaleRequestSerializer(serializers.Serializer):
    reference_payment = serializers.CharField(max_length=200)
    seller = serializers.IntegerField()
    products = serializers.ListField(child=ProductRequestSerializer())


class SaledProductSerializer(serializers.Serializer):
    gain = serializers.CharField(max_length=200)
    sale_price = serializers.FloatField()
    saled_to = serializers.FloatField()
    name = serializers.CharField(max_length=200)
    quantity = serializers.IntegerField()


class SummaryGainSellerSerializer(serializers.Serializer):
    date_sale = serializers.DateTimeField()
    reference_payment = serializers.CharField(max_length=200)
    products = SaledProductSerializer(many=True)
    sale_id = serializers.IntegerField()


class PaySellerSerializer(serializers.Serializer):
    name_seller = serializers.CharField(max_length=200)
    total_to_pay = serializers.FloatField()
    resume = serializers.ListField(child=SummaryGainSellerSerializer())
