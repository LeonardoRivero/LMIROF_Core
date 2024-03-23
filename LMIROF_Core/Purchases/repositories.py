from dataclasses import asdict
from typing import Iterable

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError, QuerySet
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Purchases.Domain.Entities import PurchaseEntity, PurchaseProductEntity
from Purchases.Domain.Interfaces import Repository
from Purchases.models import Purchase, PurchaseProduct


class PurchaseRepository(Repository):
    class SaverSerializer(serializers.ModelSerializer):
        class Meta:
            model = Purchase
            fields = "__all__"

    def add(self, entity: PurchaseEntity):
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError

    def get_by_id(self, pk: int) -> QuerySet[PurchaseEntity]:
        try:
            return Purchase.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get_all(self):
        return Purchase.objects.all()

    def update(self, entity: PurchaseEntity, pk: int) -> PurchaseEntity:
        current_record = self.get_by_id(pk)
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(current_record, data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError(serializer.errors)

    def update_partial(self, entity: dict, pk: int):
        current_record = self.get_by_id(pk)
        serializer = self.SaverSerializer(current_record, data=entity, partial=True)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError(serializer.errors)

    def delete(self, id: int) -> bool:
        try:
            response = self.get_by_id(id)
            response.delete()
            return True
        except ProtectedError:
            return False

    def find_by_parameter(self, parameters: dict) -> Iterable[PurchaseEntity]:
        data = Purchase.objects.filter(**parameters)
        if data.exists():
            return data
        return None


class PurchaseProductRepository(Repository):
    class SaverSerializer(serializers.ModelSerializer):
        class Meta:
            model = PurchaseProduct
            fields = "__all__"

    def add(self, entity: PurchaseProductEntity):
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError

    def get_by_id(self, pk: int) -> QuerySet[PurchaseProductEntity]:
        try:
            return PurchaseProduct.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get_all(self):
        return PurchaseProduct.objects.all()

    def update(self, entity: PurchaseProductEntity, pk: int) -> PurchaseProductEntity:
        current_record = self.get_by_id(pk)
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(current_record, data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError(serializer.errors)

    def update_partial(self, entity: dict, pk: int):
        current_record = self.get_by_id(pk)
        serializer = self.SaverSerializer(current_record, data=entity, partial=True)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError(serializer.errors)

    def delete(self, id: int) -> bool:
        try:
            response = self.get_by_id(id)
            response.delete()
            return True
        except ProtectedError:
            return False

    def find_by_parameter(self, parameters: dict) -> Iterable[PurchaseProductEntity]:
        data = PurchaseProduct.objects.select_related("product", "purchase").filter(
            **parameters
        )
        if data.exists():
            return data
        return None
