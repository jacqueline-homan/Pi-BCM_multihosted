from django.urls import path

from . import views

app_name = 'prefixes'
urlpatterns = [
    path('prefixes/', views.prefixes),
]