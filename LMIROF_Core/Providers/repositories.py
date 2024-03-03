from dataclasses import asdict
from typing import Iterable

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError, QuerySet
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .Domain.Entities import ProductEntity, ProviderEntity
from .Domain.Interfaces import Repository
from .models import Product, Provider


class ProviderRepository(Repository):
    class SaverSerializer(serializers.ModelSerializer):
        class Meta:
            model = Provider
            fields = "__all__"

    def add(self, entity: ProviderEntity):
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError

    def get_by_id(self, pk: int) -> QuerySet[ProviderEntity]:
        try:
            return Provider.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get_all(self):
        return Provider.objects.all()

    def update(self, entity: ProviderEntity, pk: int) -> ProviderEntity:
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

    def find_by_parameter(self, parameters: dict) -> Iterable[ProviderEntity]:
        data = Provider.objects.filter(**parameters)
        if data.exists():
            return data
        return None


class ProductRepository(Repository):
    class SaverSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = "__all__"

    def add(self, entity: ProductEntity):
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError

    def get_by_id(self, pk: int) -> Product:
        try:
            return Product.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get_all(self):
        return Product.objects.all().select_related("provider").defer('date_created', "last_modified")

    def update(self, entity: ProductEntity, pk: int) -> ProductEntity:
        current_record = self.get_by_id(pk)
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(current_record, data=entity_as_dict)
        if serializer.is_valid():
            record: ProductEntity = serializer.save()  # type: ignore
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

    def find_by_parameter(self, parameters: dict) -> QuerySet[ProductEntity]:
        data = Product.objects.filter(**parameters)
        if data.exists():
            return data
        return None
