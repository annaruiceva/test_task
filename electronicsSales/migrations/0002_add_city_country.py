# Generated by Django 4.1.3 on 2022-11-28 14:48

from django.db import migrations


class Migration(migrations.Migration):

    def populate_cities(apps, schema_editor):

        City = apps.get_model('electronicsSales', 'City')
        with open("static/txt/city.txt", encoding='utf-8') as f:
            for line in f:
                City.objects.create(name=line.replace('\n', ''))

    def populate_country(apps, schema_editor):

        Country = apps.get_model('electronicsSales', 'Country')
        with open("static/txt/country.txt", encoding='utf-8') as f:
            for line in f:
                Country.objects.create(name=line.replace('\n', ''))

    dependencies = [
        ('electronicsSales', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_cities),
        migrations.RunPython(populate_country),
    ]

