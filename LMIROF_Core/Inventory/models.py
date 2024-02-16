from django.db import models
from Providers.models import Product

# Create your models here.


class OperationType (models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=20, unique=True)

    objects = models.Manager()


class Inventory (models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    input = models.IntegerField()
    output = models.IntegerField()
    stock = models.IntegerField()
    # carrying_amount = models.DecimalField(max_digits=9, decimal_places=2)
    # operation_type = models.ForeignKey(OperationType, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=20, )
    operation_id = models.CharField(max_length=20, )
    objects = models.Manager()
