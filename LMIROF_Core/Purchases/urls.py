"""Pacientes App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from Purchases.Controllers.views import *


urlpatterns = [
    path('api/purchase/create/', CreatePurchase.as_view()),
    # path('api/seller/list/', ListSeller.as_view()),
    # path('api/sale/create/', CreateSale.as_view()),
    # path('api/sale/list/', ListSales.as_view()),
    # path('api/saleproduct/list/', ListSalesProduct.as_view()),
    # path('api/saleproduct/filter/', SearchByFilterSale.as_view()),
    path('api/purchase/<int:purchase_id>/',
         GetPurchaseByID.as_view()),
]
