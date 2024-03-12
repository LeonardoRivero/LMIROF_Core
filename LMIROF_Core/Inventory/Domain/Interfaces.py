from abc import ABC, ABCMeta, abstractmethod
from typing import Generic, Iterable, Type, TypeVar
from django.db.models.query import QuerySet
from django.db.models import Model
from ..Domain.Entities import InventoryEntity


T = TypeVar('T')


class UseCase(ABC):
    @abstractmethod
    def execute(self, payload: Generic[T]) -> Generic[T] or Iterable[Generic[T]]:
        raise NotImplementedError


class Repository(ABC):
    @abstractmethod
    def add(self, entity: object):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int) -> Type[Model]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, ):
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: object, pk: int) -> object:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def find_by_parameter(self, parameters: dict) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def update_partial(self, entity: dict, pk: int):
        raise NotImplementedError
