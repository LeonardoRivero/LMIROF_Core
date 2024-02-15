from django.db import models
from django.db import models
from Providers.models import Product, Provider

# Create your models here.


class Purchase (models.Model):
    id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,  through='PurchaseProduct')
    reference_invoice = models.CharField(max_length=90, null=False)
    tax = models.IntegerField()
    subtotal = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()


class PurchaseProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
