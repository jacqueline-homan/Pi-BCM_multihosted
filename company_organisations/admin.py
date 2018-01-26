# Register your models here.

from django.contrib import admin

from .models import CompanyOrganisation, CompanyOrganisationOwner, CompanyOrganisationUser

admin.site.register(CompanyOrganisation)
admin.site.register(CompanyOrganisationOwner)
admin.site.register(CompanyOrganisationUser)
