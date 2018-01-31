from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('add_product', views.add_product, name='add_product'),
    path('products_list', views.products_list, name='products_list'),
]