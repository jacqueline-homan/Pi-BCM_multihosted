from collections import OrderedDict

from django.contrib.admin import AdminSite

from audit.models import Log
from company_organisations.models import (
    CompanyOrganisation, CompanyOrganisationOwner, CompanyOrganisationUser
)
from prefixes.models import Prefix
from products.models import Product
from . import mo_views


# {app_label: <list-of-mo-admin-views-for-required-models>}
apps_config = OrderedDict([
    ('audit', [
        # we could override admin.site with a custom instance, it would bring standard urls
        # like add_url, but for now it's easier to adjust templates and replace urls there
        mo_views.AuditLogCustomAdmin(Log, AdminSite()),
    ]),
    ('company_organisations', [
        mo_views.CompanyOrganisationCustomAdmin(CompanyOrganisation, AdminSite()),
        mo_views.CompanyOrganisationOwnerCustomAdmin(CompanyOrganisationOwner, AdminSite()),
        mo_views.CompanyOrganisationUserCustomAdmin(CompanyOrganisationUser, AdminSite()),
    ]),
    ('prefixes', [
        mo_views.PrefixCustomAdmin(Prefix, AdminSite())
    ]),
    ('products', [
        mo_views.ProductCustomAdmin(Product, AdminSite())
    ]),
])

config = {
    'required_django_group_name': 'MO Admins',
    'apps_config': apps_config,
}
