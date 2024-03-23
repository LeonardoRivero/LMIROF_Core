from django.urls import path

from .Controllers.viewsOrders import CreateOrder, GetOrdersPending, ListOrders
from .Controllers.viewsSales import (
    CreateSale,
    FilterSale,
    GetSaleByID,
    ListSales,
    ListSalesProduct,
    SearchByFilterSale,
    SummarySalesBySeller,
)
from .Controllers.viewsSeller import CreateSeller, ListSeller

urlpatterns = [
    path("api/seller/create/", CreateSeller.as_view()),
    path("api/seller/list/", ListSeller.as_view()),
    path("api/sale/create/", CreateSale.as_view()),
    path("api/sale/list/", ListSales.as_view()),
    path("api/sale/<int:sale_id>/", GetSaleByID.as_view()),
    path("api/sale/filter/", FilterSale.as_view()),
    path("api/saleproduct/list/", ListSalesProduct.as_view()),
    path("api/saleproduct/filter/", SearchByFilterSale.as_view()),
    path("api/summaryseller/<int:seller_id>/", SummarySalesBySeller.as_view()),
    path("api/order/create/", CreateOrder.as_view()),
    path("api/order/list/", ListOrders.as_view()),
    path("api/order/pending/", GetOrdersPending.as_view()),
]
