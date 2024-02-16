from typing import List
from Purchases.Domain.Entities import PurchaseProductEntity
from ..Domain.Request import SaleRequest
from ..Domain.Interfaces import Repository, UseCase
from ..Domain.Entities import SaleEntity, SaleProductEntity
from LMIROF_Core.containers import container
from datetime import date, timedelta, timezone, datetime
from dateutil import relativedelta


class CreateSaleUseCase(UseCase):
    def __init__(self, repository_sale: Repository = container.repositories("sale"), repository_sale_product: Repository = container.repositories("sale_product")):
        self.repository_sale = repository_sale
        self.repository_sale_product = repository_sale_product

    def execute(self, request: SaleRequest) -> SaleEntity:
        sale_entity = SaleEntity(
            reference_payment=request.reference_payment, seller=request.seller)
        record: SaleEntity = self.repository_sale.add(sale_entity)
        if (record == None):
            raise TypeError()

        for item in request.products:
            product: PurchaseProductEntity = self.mediator.notify(self,
                                                                  {"product": item["id"]})
            gain = (float(item["sale_price"]) -
                    float(product.unit_price))*int(item["quantity"])
            total = (float(item["sale_price"])*int(item["quantity"]))
            sale_product_entity = SaleProductEntity(quantity=int(item["quantity"]), gain=round(gain, 2),
                                                    sale_price=float(item["sale_price"]), sale=record.id, product=item["id"], total=total)
            self.repository_sale_product.add(sale_product_entity)
        return record


class GetSalesBySellerIdUseCase(UseCase):
    def __init__(self, repository_sale: Repository = container.repositories("sale")):
        self.repository_sale = repository_sale

    def execute(self, id_seller: int) -> List[SaleEntity]:
        # current_month = datetime.now(tz=timezone.utc).date().replace(day=1)
        # next_month = current_month + relativedelta.relativedelta(months=1)
        # data = self.repository_sale.find_by_parameter(
        #     {"seller": id_seller, 'date_created__gte': current_month, 'date_created__lt': next_month})
        # return data

        today = datetime.today()
        start_week = today - timedelta(today.weekday())
        end_week = start_week + timedelta(7)
        data = self.repository_sale.find_by_parameter(
            {"seller": id_seller, 'date_created__gte': start_week.date(), 'date_created__lte': end_week.date()})
        return data
