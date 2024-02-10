from ..Domain.Request import PurchaseRequest
from ..Domain.Interfaces import Repository, UseCase
from ..Domain.Entities import SaleEntity, SellerEntity
from LMIROF_Core.containers import container


class CreateSaleUseCase(UseCase):
    def __init__(self, repository_sale: Repository = container.repositories("sale"),repository_sale_product: Repository = container.repositories("sale_product")):
        self.repository_sale = repository_sale
        self.repository_sale_product=repository_sale_product

    def execute(self, entity: PurchaseRequest) -> SaleEntity:
        record: SaleEntity = self.repository_sale.add(entity)
        if(record ==None):
            raise TypeError()
        self.repository_sale_product.add(entity)
        return record
