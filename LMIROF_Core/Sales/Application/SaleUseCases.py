import datetime
from typing import Iterable, List, Type

import dateutil.parser
from django.db.models import QuerySet
from Purchases.Domain.Entities import PurchaseProductEntity
from Sales.Domain.DTOs import SchemaBusinessDTO, SchemaSaleDTO

from ..Domain.Entities import OrderProductEntity, SaleEntity
from ..Domain.Interfaces import Repository, UseCase
from ..Domain.Request import SaleRequest, SummarySellerRequest


class CreateSaleUseCase(UseCase):
    schema_business: SchemaBusinessDTO
    schema_sale: SchemaSaleDTO

    def __init__(
        self, repository_sale: Repository, repository_order_product: Repository
    ):
        self.repository_sale = repository_sale
        self.repository_order_product = repository_order_product

    def execute(self, request: SaleRequest) -> SaleEntity:
        self.schema_sale = SchemaSaleDTO()
        self.schema_business = SchemaBusinessDTO()
        order_products: Iterable[OrderProductEntity] = (
            self.repository_order_product.find_by_parameter(
                {"order_id": request.order_id}
            )
        )

        all_purchase_products = {}
        for item in order_products:
            purchase_product: PurchaseProductEntity = self.mediator.notify(
                self, {"product": item.product_id}
            )
            self.schema_business.cost_price = round(
                self.schema_business.cost_price
                + ((purchase_product.total / purchase_product.quantity) * item.quantity)
            )
            self.schema_business.gain_business = self.schema_business.gain_business + (
                item.product.gain_business * item.quantity
            )
            self.schema_business.gain_operational = (
                self.schema_business.gain_operational
                + (item.product.gain_operational * item.quantity)
            )
            all_purchase_products.update({purchase_product.product: purchase_product})

        sale: Iterable[SaleEntity] | None = self.repository_sale.find_by_parameter(
            {"order_id": request.order_id}
        )

        if sale is not None:
            for item in sale:
                self.schema_sale.total_deposit = self.schema_sale.total_deposit + float(
                    item.total
                )
                self.schema_sale.gain_business = (
                    self.schema_sale.gain_business + item.gain_business
                )
                self.schema_sale.gain_operational = (
                    self.schema_sale.gain_operational + item.gain_operational
                )
                self.schema_sale.gain_seller = (
                    self.schema_sale.gain_seller + item.gain_seller
                )

        self.schema_sale.total_deposit = self.schema_sale.total_deposit + float(
            request.total
        )

        if request.is_cash_payment:
            return self.__is_cash_payment(request)
        return self.__is_quotas_payment(request)

    def __is_cash_payment(self, request: SaleRequest) -> SaleEntity:

        if (
            self.schema_sale.total_deposit
            < self.schema_business.gain_business
            + self.schema_business.cost_price
            + self.schema_business.gain_operational
        ):
            raise ValueError("Sale price is not allowed")
        return self.__total_deposit_is_greater_gain_operational(request)

    def __total_deposit_is_lower_cost_price(self, request: SaleRequest):
        sale_entity = SaleEntity(
            reference_payment=request.reference_payment,
            is_cash_payment=request.is_cash_payment,
            is_finish=False,
            gain_seller=0,
            gain_business=0,
            gain_operational=0,
            total=float(request.total),
            order=request.order_id,
            payment_method=request.payment_method,
            seller=1,
        )
        return self.repository_sale.add(sale_entity)

    def __total_deposit_is_between_cost_price_and_gain_business(
        self, request: SaleRequest
    ):
        if self.schema_sale.gain_business == 0:
            sale_entity = SaleEntity(
                reference_payment=request.reference_payment,
                is_cash_payment=request.is_cash_payment,
                is_finish=False,
                gain_seller=0,
                gain_business=self.schema_sale.total_deposit
                - self.schema_business.cost_price,
                gain_operational=0,
                total=request.total,
                order=request.order_id,
                payment_method=request.payment_method,
                seller=1,
            )
        else:
            sale_entity = SaleEntity(
                reference_payment=request.reference_payment,
                is_cash_payment=request.is_cash_payment,
                is_finish=False,
                gain_seller=0,
                gain_business=float(request.total),
                gain_operational=0,
                total=request.total,
                order=request.order_id,
                payment_method=request.payment_method,
                seller=1,
            )
        return self.repository_sale.add(sale_entity)

    def __total_deposit_is_greater_gain_operational(self, request: SaleRequest):
        gain_seller = (
            float(self.schema_sale.gain_seller)
            + self.schema_sale.total_deposit
            - self.schema_business.cost_price
            - self.schema_business.gain_business
            - self.schema_business.gain_operational
        )
        gain_business = self.schema_business.gain_business - float(
            self.schema_sale.gain_business
        )

        gain_operational = self.schema_business.gain_operational - float(
            self.schema_sale.gain_operational
        )
        sale_entity = SaleEntity(
            reference_payment=request.reference_payment,
            is_cash_payment=request.is_cash_payment,
            is_finish=True,
            gain_seller=gain_seller,
            gain_business=gain_business,
            gain_operational=gain_operational,
            total=float(request.total),
            order=request.order_id,
            payment_method=request.payment_method,
            seller=1,
        )
        response = self.repository_sale.add(sale_entity)
        list_sales: List[SaleEntity] = []
        sales: QuerySet[SaleEntity] = self.repository_sale.find_by_parameter(
            {"order_id": request.order_id}
        )
        for sale in sales:
            sale.is_finish = True
            sale.last_modified = datetime.datetime.today()
            list_sales.append(sale)
        sales.bulk_update(list_sales, ["is_finish", "last_modified"])
        self.mediator.toFinishOrder(request.order_id)
        return response

    def __total_deposit_is_between_gain_business_and_operational(
        self, request: SaleRequest
    ):
        gain_operational = (
            self.schema_sale.total_deposit
            - self.schema_business.cost_price
            - self.schema_business.gain_business
        )
        gain_business = self.schema_business.gain_business - float(
            self.schema_sale.gain_business
        )

        sale_entity = SaleEntity(
            reference_payment=request.reference_payment,
            is_cash_payment=request.is_cash_payment,
            is_finish=False,
            gain_seller=0,
            gain_business=gain_business,
            gain_operational=gain_operational,
            total=float(request.total),
            order=request.order_id,
            payment_method=request.payment_method,
            seller=1,
        )
        return self.repository_sale.add(sale_entity)

    def __is_quotas_payment(self, request: SaleRequest) -> SaleEntity:
        if self.schema_sale.total_deposit <= float(self.schema_business.cost_price):
            return self.__total_deposit_is_lower_cost_price(request)

        if (
            self.schema_sale.total_deposit
            <= self.schema_business.cost_price + self.schema_business.gain_business
        ):
            return self.__total_deposit_is_between_cost_price_and_gain_business(request)

        if (
            self.schema_sale.total_deposit
            >= self.schema_business.cost_price
            + self.schema_business.gain_business
            + self.schema_business.gain_operational
        ):
            return self.__total_deposit_is_greater_gain_operational(request)

        if (
            self.schema_sale.total_deposit
            <= self.schema_business.cost_price
            + self.schema_business.gain_business
            + self.schema_business.gain_operational
        ) or self.schema_sale.gain_business == 0:
            return self.__total_deposit_is_between_gain_business_and_operational(
                request
            )


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


class GetAllSalesPendingUseCase(UseCase):
    def __init__(self, repository_sale: Repository):
        self.repository_sale = repository_sale

    def execute(self) -> QuerySet:
        return self.repository_sale.find_by_parameter({"is_finish": False})
