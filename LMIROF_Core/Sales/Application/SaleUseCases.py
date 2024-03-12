from typing import List, Type

import dateutil.parser
from Providers.Domain.Entities import ProductEntity
from Purchases.Domain.Entities import PurchaseProductEntity

from ..Domain.Entities import SaleEntity, SaleProductEntity
from ..Domain.Interfaces import Repository, UseCase
from ..Domain.Request import SaleRequest, SummarySellerRequest


class CreateSaleUseCase(UseCase):
    def __init__(
        self, repository_sale: Repository, repository_sale_product: Repository
    ):
        self.repository_sale = repository_sale
        self.repository_sale_product = repository_sale_product

    def execute(self, request: SaleRequest) -> SaleEntity:
        dict_products = {}
        for item in request.products:
            response = self.mediator.getProductById(item["id"])
            dict_products.update({response.id: response})

        list_sale_product: List[SaleProductEntity] = []

        for item in request.products:
            purchase_product: PurchaseProductEntity = self.mediator.notify(
                self, {"product": item["id"]}
            )
            quantity = int(item["quantity"])
            product: ProductEntity = dict_products[item["id"]]
            cost_price = purchase_product.total/purchase_product.quantity
            sale_price = float(item["sale_total"])/quantity
            raw_gain = sale_price - float(cost_price)
            gain_seller = raw_gain - product.gain_business - product.gain_operational

            if sale_price < product.sale_price and gain_seller < 0:
                raise ValueError("Sale price is not allowed")

            sale_product = SaleProductEntity(
                quantity=quantity,
                gain_seller=round(gain_seller, 2)*quantity,
                gain_business=product.gain_business*quantity,
                sale_price=sale_price,
                sale=0,
                product=item["id"],
                total=sale_price * quantity,
                gain_operational=product.gain_operational*quantity
            )

            list_sale_product.append(sale_product)

        sale_entity = SaleEntity(
            reference_payment=request.reference_payment, seller=request.seller
        )
        record: SaleEntity = self.repository_sale.add(sale_entity)

        for sale_products in list_sale_product:
            sale_products.sale = record.id
            self.repository_sale_product.add(sale_products)
        return record


class GetSalesBySellerIdUseCase(UseCase):
    def __init__(self, repository_sale: Type[Repository]):
        self.repository_sale = repository_sale

    def execute(self, request: SummarySellerRequest) -> List[SaleEntity]:
        # current_month = datetime.now(tz=timezone.utc).date().replace(day=1)
        # next_month = current_month + relativedelta.relativedelta(months=1)
        # data = self.repository_sale.find_by_parameter(
        #     {"seller": id_seller, 'date_created__gte': current_month, 'date_created__lt': next_month})
        # return data

        # today = datetime.today()
        # start_week = today - timedelta(today.weekday())
        # end_week = start_week + timedelta(7)
        start = dateutil.parser.parse(request.start)
        end = dateutil.parser.parse(request.end)
        data = self.repository_sale.find_by_parameter(
            {
                "seller": request.id,
                "date_created__gte": start.date(),
                "date_created__lte": end.date(),
            }
        )
        return data


class GetSaleByIdUseCase(UseCase):
    def __init__(self, repository_sale: Repository):
        self.repository_sale = repository_sale

    def execute(self, sale_id: int) -> List[SaleEntity]:
        return self.repository_sale.get_by_id(sale_id)


class GetSaleByReference(UseCase):
    def __init__(self, repository_sale: Repository):
        self.repository_sale = repository_sale

    def execute(self, reference: str) -> SaleEntity:
        return self.repository_sale.find_by_parameter(
            {"reference_payment": reference.title()}
        )
