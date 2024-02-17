from typing import List
from ..Domain.DTOs import PaySellerDTO, SaledProductDTO, SummaryGainSellerDTO
from ..Domain.Interfaces import Repository, UseCase
from ..Domain.Entities import SaleEntity, SaleProductEntity, SellerEntity
from django.db.models import QuerySet


class CreateSellerUseCase(UseCase):
    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(self, entity: SellerEntity) -> SellerEntity:
        record: SellerEntity = self.repository.add(entity)
        return record


class GetSummaryGainSellerUseCase(UseCase):

    summary: List[SummaryGainSellerDTO] = []
    saled_products_dto: List[SaledProductDTO] = []
    total_to_pay: float = 0

    def __init__(self, repository_sale: Repository, repository_sale_product: Repository):
        self.repository_sale = repository_sale
        self.repository_sale_product = repository_sale_product

    def execute(self, seller_id: int) -> PaySellerDTO:
        sales: QuerySet[SaleEntity] = self.mediator.notify(self,
                                                           {"seller_id": seller_id})

        for sale in sales:
            sale_product: QuerySet = self.repository_sale_product.find_by_parameter({
                "sale": sale.id})
            self.saled_products_dto = self.__get_list_saled_products__(
                sale_product)
            summary_dto = SummaryGainSellerDTO(
                reference_payment=sale.reference_payment, date_sale=sale.date_created, sale_id=sale.id, products=self.saled_products_dto)

            self.summary.append(summary_dto)

        pay_seller_dto = PaySellerDTO(
            name_seller=self.__getSeller__(seller_id), resume=self.summary, total_to_pay=self.total_to_pay)
        return pay_seller_dto

    def __get_list_saled_products__(self, sale_product: QuerySet[SaleProductEntity]) -> List[SaledProductDTO]:
        saled_products: List[SaledProductDTO] = []

        for item in sale_product:
            gain_seller = item.gain/2
            saled_products.append(SaledProductDTO(
                gain=gain_seller, sale_price=item.sale_price, name=item.product.name))
            self.total_to_pay = self.total_to_pay + gain_seller
        return saled_products

    def __getSeller__(self, seller_id: int) -> str:
        seller: SellerEntity = self.mediator.getSellerById(seller_id)
        name_seller = "".join([seller.name, ' ', seller.last_name])
        return name_seller


class GetSellerByIdUseCase(UseCase):
    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(self, seller_id: int) -> SellerEntity:
        record: SellerEntity = self.repository.get_by_id(seller_id)
        return record
