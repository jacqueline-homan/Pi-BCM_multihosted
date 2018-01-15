from django.contrib import admin
from .models import Country, Language, LanguageByCountry
# Register your models here.

admin.site.register(Country)
admin.site.register(Language)
admin.site.register(LanguageByCountry)
