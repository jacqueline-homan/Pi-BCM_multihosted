from django.contrib import admin
from .models import Country, Language, LanguageByCountry


class LanguageByCountryAdmin(admin.ModelAdmin):
    # list_display = ('country', 'language', 'default')
    pass


#class ProfileAdmin(admin.ModelAdmin):
    # list_display = ('user', 'username', 'country', 'language')
#    pass

admin.site.register(Country)
admin.site.register(Language)
admin.site.register(LanguageByCountry, LanguageByCountryAdmin)
#admin.site.register(Profile, ProfileAdmin)
