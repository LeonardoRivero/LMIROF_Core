from dataclasses import asdict
from typing import Iterable

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError, QuerySet
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .Domain.Entities import SaleEntity, SaleProductEntity, SellerEntity
from .Domain.Interfaces import Repository
from .models import Sale, SaleProduct, Seller


class SellerRepository(Repository):
    class SaverSerializer(serializers.ModelSerializer):
        class Meta:
            model = Seller
            fields = "__all__"

    def add(self, entity: SellerEntity):
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError

    def get_by_id(self, pk: int) -> QuerySet[SellerEntity]:
        try:
            return Seller.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get_all(self):
        return Seller.objects.all()

    def update(self, entity: SellerEntity, pk: int) -> SellerEntity:
        current_record = self.get_by_id(pk)
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(current_record, data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError(serializer.errors)

    def update_partial(self, entity: dict, pk: int):
        current_record = self.get_by_id(pk)
        serializer = self.SaverSerializer(
            current_record, data=entity, partial=True)
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

    def find_by_parameter(self, parameters: dict) -> Iterable[SellerEntity]:
        data = Seller.objects.filter(**parameters)
        if (data.exists()):
            return data
        return None


class SaleRepository(Repository):
    class SaverSerializer(serializers.ModelSerializer):
        class Meta:
            model = Sale
            fields = "__all__"

    def add(self, entity: SaleEntity):
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError

    def get_by_id(self, pk: int) -> QuerySet[SaleEntity]:
        try:
            return Sale.objects.select_related("seller").prefetch_related("product").get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get_all(self):
        return Sale.objects.all()

    def update(self, entity: SaleEntity, pk: int) -> SaleEntity:
        current_record = self.get_by_id(pk)
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(current_record, data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError(serializer.errors)

    def update_partial(self, entity: dict, pk: int):
        current_record = self.get_by_id(pk)
        serializer = self.SaverSerializer(
            current_record, data=entity, partial=True)
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

    def find_by_parameter(self, parameters: dict) -> Iterable[SaleEntity]:
        data = Sale.objects.select_related(
            "seller").prefetch_related("product").filter(**parameters)
        if (data.exists()):
            return data
        return None


class SaleProductRepository(Repository):
    class SaverSerializer(serializers.ModelSerializer):
        class Meta:
            model = SaleProduct
            fields = "__all__"

    def add(self, entity: SaleProductEntity):
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError

    def get_by_id(self, pk: int) -> QuerySet[SaleProductEntity]:
        try:
            return SaleProduct.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get_all(self):
        return Sale.objects.all()

    def update(self, entity: SaleProductEntity, pk: int) -> SaleProductEntity:
        current_record = self.get_by_id(pk)
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(current_record, data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError(serializer.errors)

    def update_partial(self, entity: dict, pk: int):
        current_record = self.get_by_id(pk)
        serializer = self.SaverSerializer(
            current_record, data=entity, partial=True)
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

    def find_by_parameter(self, parameters: dict) -> Iterable[SaleProductEntity]:
        data = SaleProduct.objects.filter(**parameters)
        if (data.exists()):
            return data
        return None
