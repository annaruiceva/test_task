import random

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from mimesis import Person, Finance, Address

from electronicsSales import models

User = get_user_model()


def add_products(request):
    members = models.Element.objects.all()
    for member in members:
        try:
            provider_id = member.provider.id
            provider_products = models.Element.objects.get(id=provider_id).products.all()
            for p in provider_products:
                member.products.add(p)
        except:
            print('ошибка в продукте или поставщике', member.id)
    return redirect('/')


def fake_create_element(request):
    count_city = 100
    count_country = 60
    count_from = 20
    count_to = 39
    el_type = models.Element.DISTRIBUTOR,
    # el_type=models.Element.DEALER,
    # el_type=models.Element.RETAIL,
    # el_type = models.Element.INDIVIDUAL,
    person = Person()
    fin = Finance()
    address = Address()
    for i in range(5):
        models.Element.objects.bulk_create(
            [
                models.Element(
                    name=fin.company(),
                    type=el_type,
                    country=models.Country.objects.get(id=random.randint(1, count_country)),
                    city=models.City.objects.get(id=random.randint(1, count_city)),
                    street=address.street_name(),
                    house=address.street_number(),
                    email=person.email(),
                    debt=random.randint(1, 1000),
                    provider=models.Element.objects.get(id=random.randint(count_from, count_to))
                ),
            ]
        )
    return redirect('/')


def fake_create_user(request):
    for _ in range(2):
        person = Person('ru')
        User.objects.create(
            username=person.username(),
            email=person.email(),
            first_name=person.first_name(),
            last_name=person.last_name(),
            password=make_password(person.password(length=8)),
        )
    return redirect('/')
