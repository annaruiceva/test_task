import re

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import permissions
from rest_framework import serializers

#
# User = get_user_model()


from electronicsSales.models import Element, Product


class MemberModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = Element
        fields = ('id', 'type', 'name', 'city', 'country', 'debt', 'provider', 'products')


class UpdateMemberModelSerializer(serializers.ModelSerializer):
    debt = serializers.ReadOnlyField()

    class Meta:
        model = Element
        fields = ('id', 'type', 'name', 'city', 'country', 'debt', 'provider', 'products')


class MembersModelSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name')
    country = serializers.CharField(source='country.name')

    class Meta:
        model = Element
        fields = ('id', 'type', 'name', 'city', 'country', 'debt', 'provider')


class MemberSmallModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ('id', 'name')


class MemberSmallDebtModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        depth = 1
        fields = ('id', 'name', 'debt', 'products')


class ProductsModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name.name')

    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'release_date')


class ProductsIntModelSerializer(serializers.ModelSerializer):
    model = serializers.CharField(max_length=25)
    release_date = serializers.DateField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'release_date')


class MemberContactSerializer(serializers.ModelSerializer):
    city = serializers.ReadOnlyField(source='city.name')
    country = serializers.ReadOnlyField(source='country.name')

    class Meta:
        model = Element
        fields = ('id', 'city', 'country', 'email', 'street', 'house')
