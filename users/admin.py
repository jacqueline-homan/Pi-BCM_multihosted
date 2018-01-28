from django.contrib import admin
from .models import User


class UsersModelAdmin(admin.ModelAdmin):
    list_display = ( 'user', )


admin.site.register(User, UsersModelAdmin)
