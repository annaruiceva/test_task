from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response

from electronicsSales import models
from electronicsSales.api.serializers import MembersModelSerializer, \
    ProductsModelSerializer, ProductsIntModelSerializer, MemberSmallModelSerializer, MemberModelSerializer, \
    MemberSmallDebtModelSerializer, UpdateMemberModelSerializer, MemberContactSerializer
# @api_view(['GET'])
# def members_api(request):
#     if not request.user.is_anonymous:
#         if request.method == 'GET':
#             members = models.Element.objects.all()
#             serializer = MembersModelSerializer(members, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response({'detail': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
from electronicsSales.tasks import send_email
from electronicsSales.utils import create_qr_code


class MemberListAPIView(generics.ListCreateAPIView):
    """просмотр и создание нового объекта"""

    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MembersModelSerializer
        return MemberModelSerializer

    queryset = models.Element.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country__name', 'country']
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class MemberListProductFilterAPIView(generics.ListCreateAPIView):
    """просмотр объектов с продуктом"""

    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MemberSmallModelSerializer
        return MemberModelSerializer

    queryset = models.Element.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['products']
    permission_classes = [permissions.IsAuthenticated]


class MemberDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение и удаление"""
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MemberSmallModelSerializer
        return UpdateMemberModelSerializer

    queryset = models.Element.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ProductsListAPIView(generics.ListCreateAPIView):
    """просмотр и создание нового продукта"""

    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductsModelSerializer
        return ProductsIntModelSerializer

    queryset = models.Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение и удаление"""
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductsModelSerializer
        return ProductsIntModelSerializer

    queryset = models.Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def debtors_api(request):
    if request.method == 'GET':
        if not request.user.is_anonymous:
            avg_debt = models.Element.objects.all().aggregate(Avg('debt'))
            members = models.Element.objects.filter(debt__gte=avg_debt['debt__avg'])
            serializer = MemberSmallDebtModelSerializer(members, many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def mail_api(request, pk):
    try:
        member = models.Element.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MemberContactSerializer(member)
        img_name = create_qr_code(serializer.data)
        if img_name == '':
            return Response({'detail': 'qr-code error'}, status=status.HTTP_404_NOT_FOUND)
        print(img_name)
        send_email.delay(user_id=request.user.id, img_name=img_name)
        return Response(serializer.data)
