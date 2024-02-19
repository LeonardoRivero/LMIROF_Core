from abc import ABC, ABCMeta, abstractmethod
from typing import Generic, Iterable, TypeVar
from django.db.models.query import QuerySet

from Providers.Domain.Entities import ProductEntity
from ..Domain.Entities import SellerEntity


T = TypeVar('T')


class Mediator(ABC):

    def notify(self, sender: object, event: dict) -> None:
        pass

    def getSellerById(self, seller_id: int) -> SellerEntity:
        pass
    def getProductById(self, product_id: int) -> ProductEntity:
        pass

    def getProductById(self, product_id: int) -> ProductEntity:
        pass


class UseCase(ABC):

    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator

    @abstractmethod
    def execute(self, payload: Generic[T]) -> Generic[T] or Iterable[Generic[T]]:
        raise NotImplementedError

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator


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
