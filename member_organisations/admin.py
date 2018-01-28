from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import MemberOrganisation, MemberOrganisationOwner, MemberOrganisationUser

admin.site.register(MemberOrganisation)
admin.site.register(MemberOrganisationOwner)
admin.site.register(MemberOrganisationUser)