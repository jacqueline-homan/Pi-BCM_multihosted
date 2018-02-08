from member_organisations.custom_admin.base_views import BaseCustomAdminMethods


URL_PREFIX = 'go_admin'


class CountryCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False


class LanguageCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False


class LanguageByCountryCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False


class MemberOrganisationCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False

    related_models_actions = {
        # EXAMPLE: it's possible to enable/disable links for related models here
        'member_organisation': {
            'can_add_related': False,
            'can_change_related': False,
            'can_delete_related': False,
        }
    }


class MemberOrganisationUserCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False


class MemberOrganisationOwnerCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False


class CompanyOrganisationCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False


class CompanyOrganisationOwnerCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False


class CompanyOrganisationUserCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False


class PrefixCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False


class ProductCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False


class AuditLogCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    raise_not_implemented_queryset_exception = False
