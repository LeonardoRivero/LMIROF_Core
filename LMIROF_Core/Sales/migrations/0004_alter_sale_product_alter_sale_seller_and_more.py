# Generated by Django 4.1 on 2024-03-03 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Settings', '0002_distributionproducttype'),
        ('Providers', '0004_alter_product_distribution_type_and_more'),
        ('Sales', '0003_rename_gain_saleproduct_gain_business_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='product',
            field=models.ManyToManyField(related_name='sales', through='Sales.SaleProduct', to='Providers.product'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sales', to='Sales.seller'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellers', to='Settings.gender'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='identification_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellers', to='Settings.idtype'),
        ),
    ]
