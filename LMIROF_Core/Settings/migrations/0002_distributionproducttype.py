# Generated by Django 4.1 on 2024-02-19 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistributionProductType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('profit_seller', models.FloatField()),
                ('profit_bussiness', models.FloatField()),
                ('profit_operational', models.FloatField()),
            ],
        ),
    ]
