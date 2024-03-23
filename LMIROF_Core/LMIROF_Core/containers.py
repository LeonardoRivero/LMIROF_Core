from dependency_injector import containers, providers
from Inventory import models as models_inventory
from Inventory import repositories as repos_inventory
from Inventory import serializers as serializers_inventory
from Providers import models as models_provider
from Providers import repositories as repos_providers
from Providers import serializers as serializers_providers
from Purchases import models as models_purchases
from Purchases import repositories as repos_purchases
from Purchases import serializers as serializers_purchases
from Sales import models as models_sales
from Sales import repositories as repos_sales
from Sales import serializers as serializers_sales


class Container(containers.DeclarativeContainer):

    repositories: providers.Aggregate = providers.Aggregate(
        provider=providers.Singleton(repos_providers.ProviderRepository),
        product=providers.Singleton(repos_providers.ProductRepository),
        seller=providers.Singleton(repos_sales.SellerRepository),
        sale=providers.Singleton(repos_sales.SaleRepository),
        sale_product=providers.Singleton(repos_sales.SaleProductRepository),
        purchase=providers.Singleton(repos_purchases.PurchaseRepository),
        purchase_product=providers.Singleton(repos_purchases.PurchaseProductRepository),
        inventory=providers.Singleton(repos_inventory.InventoryRepository),
        order=providers.Singleton(repos_sales.OrderRepository),
        order_product=providers.Singleton(repos_sales.OrderProductRepository),
    )

    provider_serializer = providers.Object(serializers_providers.ProviderSerializer)
    product_serializer = providers.Object(serializers_providers.ProductSerializer)
    seller_serializer = providers.Object(serializers_sales.SellerSerializer)
    sale_serializer = providers.Object(serializers_sales.SaleSerializer)
    sale_request_serializer = providers.Object(serializers_sales.SaleRequestSerializer)
    sale_product_serializer = providers.Object(serializers_sales.SaleProductSerializer)
    purchase_serializer = providers.Object(serializers_purchases.PurchaseSerializer)
    purchase_request_serializer = providers.Object(
        serializers_purchases.PurchaseRequestSerializer
    )
    inventory_serializer = providers.Object(serializers_inventory.InventorySerializer)
    payseller_serializer = providers.Object(serializers_sales.PaySellerSerializer)
    order_product_request_serializer = providers.Object(
        serializers_sales.OrderRequestSerializer
    )
    order_serializer = providers.Object(serializers_sales.OrderSerializer)

    model_provider = providers.Object(models_provider.Provider)
    model_product = providers.Object(models_provider.Product)
    model_seller = providers.Object(models_sales.Seller)
    model_sale = providers.Object(models_sales.Sale)
    model_sale_product = providers.Object(models_sales.SaleProduct)
    model_purchase_product = providers.Object(models_purchases.PurchaseProduct)
    model_inventory = providers.Object(models_inventory.Inventory)
    model_purchase = providers.Object(models_purchases.Purchase)
    model_order = providers.Object(models_sales.Order)


container = Container()
