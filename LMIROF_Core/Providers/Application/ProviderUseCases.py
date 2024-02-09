from ..Domain.Interfaces import Repository, UseCase
from ..Domain.Entities import ProductEntity, ProviderEntity
from LMIROF_Core.containers import container
from django.db.models import QuerySet
from typing import Iterable


class CreateProviderUseCase(UseCase):
    def __init__(self, repository: Repository = container.repositories("provider")):
        self.repository = repository

    def execute(self, entity: ProviderEntity) -> ProviderEntity:
        record: ProviderEntity = self.repository.add(entity)
        return record


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
