from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductName(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return 'Product name: ' + self.name


class Product(models.Model):
    name = models.ForeignKey(ProductName, on_delete=models.PROTECT)
    model = models.CharField(max_length=50)
    release_date = models.DateField()

    def __str__(self):
        return 'Product: ' + self.model


class Country(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return 'Country: ' + self.name


class City(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return 'City: ' + self.name


class Element(models.Model):
    FACTORY = "factory"
    DISTRIBUTOR = "distributor"
    DEALER = "dealer"
    RETAIL = "large"
    INDIVIDUAL = "individual"
    ELEMENTS_NAME = [
        (FACTORY, 'Factory'),
        (DISTRIBUTOR, 'Distributor'),
        (DEALER, 'Dealer center'),
        (RETAIL, 'Large retail chain'),
        (INDIVIDUAL, 'Individual entrepreneur'),
    ]

    name = models.CharField(max_length=50)
    type = models.CharField(choices=ELEMENTS_NAME, max_length=12, default=FACTORY)
    created = models.DateField(auto_now_add=True)

    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    street = models.CharField(max_length=60)
    house = models.IntegerField(default=0)
    corps = models.CharField(max_length=5, blank=True, default='')
    email = models.EmailField()

    products = models.ManyToManyField(Product, blank=True)

    debt = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    provider = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True
    )
    phone = models.CharField(max_length=20, blank=True, default='')
    member = models.ForeignKey(Element, on_delete=models.SET_NULL, blank=True, null=True, related_name='workers')

# @receiver(post_save, sender=Element)
# def add_product_to_customer(sender, instance, created, **kwargs):
#     print('add product to: ', sender)
#
#     if created:
#         print('created', instance)
#         provider_id = instance.provider.id
#         print(provider_id)
#         provider_products = Element.objects.get(id=provider_id).products.all()
#         print(provider_products)
#         for p in provider_products:
#             instance.products.add(p)
#         print('kwargs', kwargs)
