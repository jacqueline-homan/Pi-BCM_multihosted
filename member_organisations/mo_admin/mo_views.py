from functools import update_wrapper

from django.contrib import admin
from django.urls import path, reverse
from .base_views import BaseMOAdmin


# BaseMOAdmin can be used directly in case you don't need to override view methods

class AuditLogMOAdmin(BaseMOAdmin):
    pass


class CompanyOrganisationMOAdmin(BaseMOAdmin):
    pass


class CompanyOrganisationOwnerMOAdmin(BaseMOAdmin):
    pass


class CompanyOrganisationUserMOAdmin(BaseMOAdmin):
    pass


class PrefixMOAdmin(BaseMOAdmin):
    pass


class ProductMOAdmin(BaseMOAdmin):
    pass
