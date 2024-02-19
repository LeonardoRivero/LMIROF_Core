from django.db import models

# Create your models here.


class IDType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, null=False)
    abbreviation = models.CharField(max_length=10, null=False)

    objects = models.Manager()


class Gender(models.Model):
    id = models.AutoField(primary_key=True)
    name_gender = models.CharField(max_length=50, null=False)
    objects = models.Manager()


class OperationType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, null=False)
    objects = models.Manager()


class DistributionProductType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50, null=False)
    profit_seller = models.FloatField()
    profit_bussiness = models.FloatField()
    profit_operational = models.FloatField()
    objects = models.Manager()
