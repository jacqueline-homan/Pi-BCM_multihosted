"""BCM_multihosted URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from gs1ie.views import account_create_or_update, api_auth
from user.views import profile

urlpatterns = [
    path('API/v1/AccountCreateOrUpdate/', account_create_or_update),
    path('API/v1/auth/<token>/', api_auth, name='api_auth_v1'),
    path('profile/', profile, name='profile'),
    path('gs1ie/', include('gs1ie.urls')),
    path('prefixes/', include('prefixes.urls')),
    path('user/', include('user.urls')),
    path('admin/', admin.site.urls),
]
