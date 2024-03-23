from abc import ABC, abstractmethod
from typing import Generic, Iterable, Type, TypeVar

from django.db.models import Model
from django.db.models.query import QuerySet
from Providers.Domain.Entities import ProductEntity
from Sales.Domain.Request import SummarySellerRequest

from ..Domain.Entities import SellerEntity

T = TypeVar("T")


class Mediator(ABC):

    def notify(self, sender: object, event: dict) -> None:
        pass

    def getSellerById(self, seller_id: int) -> SellerEntity:
        pass

    def getProductById(self, product_id: int) -> ProductEntity:
        pass

    def getResumeSalesSeller(self, request: SummarySellerRequest):
        pass

    def getAllOrdersPending(self) -> QuerySet:
        pass

    def toFinishOrder(self, id_order: int) -> SellerEntity:
        pass


class UseCase(ABC):

    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator

    @abstractmethod
    def execute(self, payload: Generic[T]) -> Generic[T] or Iterable[Generic[T]]:  # type: ignore
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
    def get_by_id(self, id: int) -> Type[Model]:
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
    ):
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: object, pk: int) -> object:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def find_by_parameter(self, parameters: dict) -> QuerySet | None:
        raise NotImplementedError

    @abstractmethod
    def update_partial(self, entity: dict, pk: int):
        raise NotImplementedError
