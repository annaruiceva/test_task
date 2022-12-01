from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

# api
from electronicsSales.api import views

urlpatterns = [
    # API
    path('objects/', views.MemberListAPIView.as_view()),
    path('objects-product/', views.MemberListProductFilterAPIView.as_view()),
    path('product/', views.ProductsListAPIView.as_view()),
    path('product/<int:pk>', views.ProductDetailAPIView.as_view()),
    path('object/<int:pk>', views.MemberDetailAPIView.as_view()),
    path('debtors/', views.debtors_api),
    path('email_object_info/<int:pk>', views.mail_api),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'csv'])
