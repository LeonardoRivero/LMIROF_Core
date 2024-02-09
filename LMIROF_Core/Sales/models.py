from django.db import models
from Providers.models import Product, Provider
from Settings.models import Gender, IDType


# Create your models here.


class Seller (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90, null=False)
    last_name = models.CharField(max_length=90, null=False)
    identification_type = models.ForeignKey(IDType, on_delete=models.CASCADE)
    identification = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=20, unique=True)
    address = models.CharField(max_length=50)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    status = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.last_name = self.last_name.capitalize()
        super(Seller, self).save(*args, **kwargs)


class Sale (models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,  through='SaleProduct')
    reference_payment = models.CharField(max_length=90, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()


class Purchase (models.Model):
    id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    invoice_id = models.CharField(max_length=90, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()


class SaleProduct(models.Model):
    quantity = models.IntegerField()
    gain = models.DecimalField(max_digits=9, decimal_places=2)
    sale_price = models.DecimalField(max_digits=9, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
