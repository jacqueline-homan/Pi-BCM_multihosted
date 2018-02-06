from collections import OrderedDict

from django.contrib import admin
from django.contrib.auth.models import Group

from audit.models import Log
from company_organisations.models import (
    CompanyOrganisation, CompanyOrganisationOwner, CompanyOrganisationUser
)
from prefixes.models import Prefix
from products.models import Product
from . import mo_views


required_django_group, is_created = Group.objects.get_or_create(name='MO Admins')

# {app_label: <list-of-mo-admin-views-for-required-models>}
apps_config = OrderedDict([
    ('audit', [
        # we could override admin.site with a custom instance, it would bring standard urls
        # like add_url, but for now it's easier to adjust templates and replace urls there
        mo_views.AuditLogCustomAdmin(Log, admin.site),
    ]),
    ('company_organisations', [
        mo_views.CompanyOrganisationCustomAdmin(CompanyOrganisation, admin.site),
        mo_views.CompanyOrganisationOwnerCustomAdmin(CompanyOrganisationOwner, admin.site),
        mo_views.CompanyOrganisationUserCustomAdmin(CompanyOrganisationUser, admin.site),
    ]),
    ('prefixes', [
        mo_views.PrefixCustomAdmin(Prefix, admin.site)
    ]),
    ('products', [
        mo_views.ProductCustomAdmin(Product, admin.site)
    ]),
])

config = {
    'required_django_group': required_django_group,
    'apps_config': apps_config,
}
