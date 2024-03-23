from django.db import models
from Providers.models import Product
from Settings.models import Gender, IDType, PaymentMethod

# Create your models here.


class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90, null=False)
    last_name = models.CharField(max_length=90, null=False)
    identification_type = models.ForeignKey(
        IDType, on_delete=models.CASCADE, related_name="sellers"
    )
    identification = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=20, unique=True)
    address = models.CharField(max_length=50)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name="sellers")
    status = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.last_name = self.last_name.capitalize()
        super(Seller, self).save(*args, **kwargs)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.DO_NOTHING)
    product = models.ManyToManyField(
        Product, through="OrderProduct", related_name="orders"
    )
    total = models.DecimalField(max_digits=9, decimal_places=2)
    is_finish = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)


class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(
        Seller, on_delete=models.DO_NOTHING, related_name="sales"
    )
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name="sales")
    reference_payment = models.CharField(max_length=90, null=False)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)
    is_cash_payment = models.BooleanField()
    is_finish = models.BooleanField()
    gain_seller = models.DecimalField(max_digits=9, decimal_places=2)
    gain_business = models.DecimalField(max_digits=9, decimal_places=2)
    gain_operational = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()


class SaleProduct(models.Model):
    quantity = models.IntegerField()
    gain_seller = models.DecimalField(max_digits=9, decimal_places=2)
    gain_business = models.DecimalField(max_digits=9, decimal_places=2)
    gain_operational = models.DecimalField(max_digits=9, decimal_places=2)
    sale_price = models.DecimalField(max_digits=9, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2)
