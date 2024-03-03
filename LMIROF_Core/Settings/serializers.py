from rest_framework import serializers

from Settings.models import DistributionProductType, IDType


class IDTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDType
        fields = '__all__'


class DistributionProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionProductType
        fields = '__all__'
