from django.urls import path

from . import views

app_name = 'prefixes'
urlpatterns = [
    path('', views.prefixes_list, name='prefixes_list'),
    path('prefixes/', views.prefixes_list),
    path('prefixes_set_starting/<int:prefix_id>', views.prefixes_set_starting, name='prefixes_set_starting'),
]