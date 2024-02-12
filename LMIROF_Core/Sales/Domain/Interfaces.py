from abc import ABC, ABCMeta, abstractmethod
from typing import Generic, Iterable, TypeVar
from django.db.models.query import QuerySet


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
    def get_by_id(self, id: int) -> object:
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


class Mediator(ABC):

    def notify(self, sender: UseCase, event: dict) -> None:
        pass
