from ..Domain.Interfaces import Repository, UseCase
from ..Domain.Entities import SellerEntity
from LMIROF_Core.containers import container


class CreateSellerUseCase(UseCase):
    def __init__(self, repository: Repository = container.repositories("seller")):
        self.repository = repository

    def execute(self, entity: SellerEntity) -> SellerEntity:
        record: SellerEntity = self.repository.add(entity)
        return record
