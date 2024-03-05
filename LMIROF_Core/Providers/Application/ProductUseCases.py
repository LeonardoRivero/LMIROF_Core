from typing import Iterable

from django.db.models import QuerySet

from LMIROF_Core.containers import container

from ..Domain.Entities import ProductEntity
from ..Domain.Interfaces import Repository, UseCase


class CreateProductUseCase(UseCase):
    def __init__(self, repository: Repository = container.repositories("product")):
        self.repository = repository

    def execute(self, entity: ProductEntity) -> ProductEntity:
        record: ProductEntity = self.repository.add(entity)
        return record


class GetProductByNameUseCase(UseCase):
    def __init__(self, repository: Repository = container.repositories("product")):
        self.repository = repository

    def execute(self, name: str) -> Iterable[ProductEntity]:
        record: QuerySet = self.repository.get_all()
        product = record.filter(name__icontains=name, status=True)
        return product


class GetProductByIdUseCase(UseCase):
    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(self, id: int) -> ProductEntity:
        record: ProductEntity = self.repository.get_by_id(id)  # type: ignore
        if record.status is False:
            raise ValueError("Product is disabled")
        return record
