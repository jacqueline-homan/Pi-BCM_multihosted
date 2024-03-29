from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('products_add_product', views.products_add_product, name='products.add_product'),
    path('products_products_list', views.products_products_list, name='products.products_list'),
    path('static_views_terms', views.static_views_terms, name='static_views.terms'),
    path('prefixes_prefixes_list', views.prefixes_prefixes_list, name='prefixes.prefixes_list'),
    path('auth_profile', views.auth_profile, name='auth_profile'),
    path('excel_export_select', views.excel_export_select, name='excel.export_select'),
    path('excel_import_file', views.excel_import_file, name='excel.import_file'),
    path('locations_locations_list', views.locations_locations_list, name='locations.locations_list'),
]
