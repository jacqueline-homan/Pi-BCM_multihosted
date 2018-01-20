from django.contrib import admin
from .models import Country, Language, LanguageByCountry, Profile


class LanguageByCountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'language', 'default')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'country', 'language')


admin.site.register(Country)
admin.site.register(Language)
admin.site.register(LanguageByCountry, LanguageByCountryAdmin)
admin.site.register(Profile, ProfileAdmin)
