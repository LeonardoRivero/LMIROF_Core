from ..Domain.Interfaces import Repository, UseCase
from ..Domain.Entities import ProviderEntity
from LMIROF_Core.containers import container


class CreateProviderUseCase(UseCase):
    def __init__(self, repository: Repository = container.repositories("provider")):
        self.repository = repository

    def execute(self, entity: ProviderEntity) -> ProviderEntity:
        record: ProviderEntity = self.repository.add(entity)
        return record
