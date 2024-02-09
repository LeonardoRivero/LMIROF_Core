from rest_framework import serializers

from Settings.models import IDType

class IDTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDType
        fields = '__all__'