# Generated by Django 4.1 on 2024-02-16 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseproduct',
            name='product',
        ),
        migrations.RemoveField(
            model_name='purchaseproduct',
            name='purchase',
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
        migrations.DeleteModel(
            name='PurchaseProduct',
        ),
    ]
