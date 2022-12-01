# Generated by Django 4.1.3 on 2022-11-28 14:48

from django.db import migrations
from mimesis import Hardware, Datetime


class Migration(migrations.Migration):

    def fake_create_product(apps, schema_editor):
        Product = apps.get_model('electronicsSales', 'Product')
        ProductName = apps.get_model('electronicsSales', 'ProductName')
        hardware = Hardware()
        date = Datetime()
        for i in range(10):

            Product.objects.bulk_create(
                [
                    Product(
                        name=ProductName.objects.get(id=1),
                        model=hardware.phone_model(),
                        release_date=date.date(start=2018, end=2022)
                    ),
                    Product(
                        name=ProductName.objects.get(id=2),
                        model=hardware.graphics(),
                        release_date=date.date(start=2018, end=2022)
                    ),
                    Product(
                        name=ProductName.objects.get(id=3),
                        model=hardware.cpu(),
                        release_date=date.date(start=2018, end=2022)
                    ),
                ]
            )

    dependencies = [
        ('electronicsSales', '0003_add_name_product'),
    ]

    operations = [
        migrations.RunPython(fake_create_product),
    ]
