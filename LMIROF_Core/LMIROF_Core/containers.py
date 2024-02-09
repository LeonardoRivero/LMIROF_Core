from dependency_injector import containers, providers

from Providers import repositories as repos_providers
from Providers import serializers as serializers_providers
from Providers import models as models_provider


class Container(containers.DeclarativeContainer):

    repositories = providers.Aggregate(provider=providers.Singleton(repos_providers.ProviderRepository),
                                       product=providers.Singleton(repos_providers.ProductRepository))

    provider_serializer = providers.Object(
        serializers_providers.ProviderSerializer)
    product_serializer = providers.Object(
        serializers_providers.ProductSerializer)

    model_provider = providers.Object(models_provider.Provider)
    model_product = providers.Object(models_provider.Product)


container = Container()
