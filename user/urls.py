from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('profile/', views.profile),
    path('products_add_product', views.products_add_product, name='products.add_product'),
    path('products_products_list', views.products_products_list, name='products.products_list'),
    path('static_views_terms', views.static_views_terms, name='static_views.terms'),
    path('prefixes_prefixes_list', views.prefixes_prefixes_list, name='prefixes.prefixes_list'),
]
