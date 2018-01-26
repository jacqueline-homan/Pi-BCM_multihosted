from django.urls import path

from . import views

app_name = 'prefixes'
urlpatterns = [
    path('', views.prefixes_list, name='prefixes_list'),
    path('ajax/', views.prefixes_ajax),
    path('prefixes_set_starting/<int:prefix_id>', views.prefixes_set_starting, name='prefixes_set_starting'),
]