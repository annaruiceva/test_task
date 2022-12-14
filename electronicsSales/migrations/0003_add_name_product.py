# Generated by Django 4.1.3 on 2022-11-28 14:48

from django.db import migrations


class Migration(migrations.Migration):

    def product_category(apps, schema_editor):

        ProductName = apps.get_model('electronicsSales', 'ProductName')

        ProductName.objects.create(name='Телефон')
        ProductName.objects.create(name='Видеокарта')
        ProductName.objects.create(name='Процессор')

    dependencies = [
        ('electronicsSales', '0002_add_city_country'),
    ]

    operations = [
        migrations.RunPython(product_category),
    ]

