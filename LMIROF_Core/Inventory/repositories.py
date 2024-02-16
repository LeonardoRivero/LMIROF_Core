from rest_framework.exceptions import ValidationError
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from .models import Inventory
from rest_framework import serializers
from .Domain.Interfaces import Repository
from .Domain.Entities import InventoryEntity
from dataclasses import asdict
from typing import Iterable


class InventoryRepository(Repository):
    class SaverSerializer(serializers.ModelSerializer):
        class Meta:
            model = Inventory
            fields = "__all__"

    def add(self, entity: InventoryEntity):
        entity_as_dict = asdict(entity)
        serializer = self.SaverSerializer(data=entity_as_dict)
        if serializer.is_valid():
            record = serializer.save()
            return record
        raise ValidationError

    def get_by_id(self, pk: int) -> QuerySet[InventoryEntity]:
        try:
            return Inventory.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get_all(self):
        return Inventory.objects.all()

    def update(self, entity: InventoryEntity, pk: int) -> InventoryEntity:
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
        raise NotImplementedError()

    def find_by_parameter(self, parameters: dict) -> Iterable[InventoryEntity]:
        data = Inventory.objects.filter(**parameters)
        if (data.exists()):
            return data
        return None
