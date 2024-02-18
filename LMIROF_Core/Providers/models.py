from django.db import models
from cities_light.models import Country, SubRegion, Region
from Settings.models import DistributionProductType, IDType

# Create your models here.


class Provider (models.Model):
    id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=90, null=False)
    identification_type = models.ForeignKey(IDType, on_delete=models.CASCADE)
    identification = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=20, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    department = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(SubRegion, on_delete=models.CASCADE)
    email = models.EmailField()
    status = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.business_name = self.business_name.title()
        super(Provider, self).save(*args, **kwargs)


class Product (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90, null=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    reference = models.CharField(max_length=20)
    status = models.BooleanField()
    distribution_type = models.ForeignKey(DistributionProductType, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(Product, self).save(*args, **kwargs)
