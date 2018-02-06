from collections import OrderedDict

from django.contrib import admin
from django.contrib.auth.models import Group

from audit.models import Log
from member_organisations.models import (
    MemberOrganisation, MemberOrganisationUser, MemberOrganisationOwner
)
from company_organisations.models import (
    CompanyOrganisation, CompanyOrganisationOwner, CompanyOrganisationUser
)
from BCM.models import Country, Language, LanguageByCountry
from prefixes.models import Prefix
from products.models import Product
from . import go_views


def get_required_django_group():
    required_django_group, is_created = Group.objects.get_or_create(name='GO Admins')
    return required_django_group


# {app_label: <list-of-mo-admin-views-for-required-models>}
apps_config = OrderedDict([
    ('audit', [
        # we could override admin.site with a custom instance, it would bring standard urls
        # like add_url, but for now it's easier to adjust templates and replace urls there
        go_views.AuditLogCustomAdmin(Log, admin.site),
    ]),
    ('BCM', [
        go_views.CountryCustomAdmin(Country, admin.site),
        go_views.LanguageCustomAdmin(Language, admin.site),
        go_views.LanguageByCountryCustomAdmin(LanguageByCountry, admin.site),
    ]),
    ('member_organisations', [
        go_views.MemberOrganisationCustomAdmin(MemberOrganisation, admin.site),
        go_views.MemberOrganisationUserCustomAdmin(MemberOrganisationUser, admin.site),
        go_views.MemberOrganisationOwnerCustomAdmin(MemberOrganisationOwner, admin.site),
    ]),
    ('company_organisations', [
        go_views.CompanyOrganisationCustomAdmin(CompanyOrganisation, admin.site),
        go_views.CompanyOrganisationOwnerCustomAdmin(CompanyOrganisationOwner, admin.site),
        go_views.CompanyOrganisationUserCustomAdmin(CompanyOrganisationUser, admin.site),
    ]),
    ('prefixes', [
        go_views.PrefixCustomAdmin(Prefix, admin.site)
    ]),
    ('products', [
        go_views.ProductCustomAdmin(Product, admin.site)
    ]),
])

config = {
    'required_django_group_name': 'GO Admins',
    'apps_config': apps_config,
}
