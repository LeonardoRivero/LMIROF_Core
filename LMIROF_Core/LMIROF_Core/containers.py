from dependency_injector import containers, providers

from Providers import repositories as repos_providers
from Providers import serializers as serializers_providers
from Providers import models as models_provider
from Sales import repositories as repos_sales
from Sales import serializers as serializers_sales
from Sales import models as models_sales


class Container(containers.DeclarativeContainer):

    repositories = providers.Aggregate(provider=providers.Singleton(repos_providers.ProviderRepository),
                                       product=providers.Singleton(
                                           repos_providers.ProductRepository),
                                       seller=providers.Singleton(repos_sales.SellerRepository))

    provider_serializer = providers.Object(
        serializers_providers.ProviderSerializer)
    product_serializer = providers.Object(
        serializers_providers.ProductSerializer)
    seller_serializer = providers.Object(
        serializers_sales.SellerSerializer)

    model_provider = providers.Object(models_provider.Provider)
    model_product = providers.Object(models_provider.Product)
    model_seller = providers.Object(models_sales.Seller)


container = Container()
