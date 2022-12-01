from django.urls import path

from electronicsSales import views

urlpatterns = [
    path('add_products/', views.add_products),
    path('add_elements/', views.fake_create_element),
    path('fake-users/', views.fake_create_user),

]
