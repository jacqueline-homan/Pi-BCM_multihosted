from django.contrib import admin
from .models import Profile


class UsersModelAdmin(admin.ModelAdmin):
    list_display = ('user',)
    pass


admin.site.register(Profile, UsersModelAdmin)
