from django.urls import path

from . import views

app_name = 'gs1ie'
urlpatterns = [
    path('AccountCreateOrUpdate/', views.account_create_or_update),
]
