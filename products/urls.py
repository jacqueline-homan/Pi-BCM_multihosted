from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('products_list/', views.products_list, name='products_list'),
    path('add_product_package_type/', views.add_product_package_type, name='add_product_package_type'),
    path('add_product_base_details/', views.add_product_base_details, name='add_product_base_details'),
    path('add_product_select_sub/', views.add_product_select_sub, name='add_product_select_sub')
]
