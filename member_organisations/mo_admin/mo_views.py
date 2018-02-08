from member_organisations.mo_admin.helpers import get_allowed_mo_for_mo_admin
from member_organisations.custom_admin.base_views import BaseCustomAdminMethods


URL_PREFIX = 'mo_admin'


class AuditLogCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX

    @classmethod
    def get_audit__log_queryset(cls, request, queryset):
        # todo: there are no fields to filter this model!
        return queryset


class CompanyOrganisationCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX
    related_models_actions = {
        # it's possible to enable/disable links for related models here
        'member_organisation': {
            'can_add_related': False,
            'can_change_related': False,
            'can_delete_related': False,
        }
    }

    @classmethod
    def get_company_organisations__companyorganisation_queryset(cls, request, queryset):
        """
        name convention:
            "get_{model._meta.app_label}__{model._meta.model_name}_queryset".lower()

        if a method doesn't exist you'll recieve the exception
        with a required method and class names
        """

        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(member_organisation__in=allowed_organizations)
        return queryset

    @classmethod
    def get_bcm__country_queryset(cls, request, queryset):
        return queryset

    @classmethod
    def get_member_organisations__memberorganisation_queryset(cls, request, queryset):
        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(pk__in=allowed_organizations)
        return queryset


class CompanyOrganisationOwnerCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX

    @classmethod
    def get_company_organisations__companyorganisationowner_queryset(cls, request, queryset):
        """
        queryset filtering for CO owners changelist
        link: "/mo_admin/company_organisations_companyorganisationowner/"
        """

        # filter by organization, company organization should belong to request.user MO
        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(organization__member_organisation__in=allowed_organizations)

        # filter by user, organization user should belong to CO, which belong to request.user MO
        queryset = queryset.filter(
            organization_user__organization__member_organisation__in=allowed_organizations
        )
        return queryset

    @classmethod
    def get_company_organisations__companyorganisationuser_queryset(cls, request, queryset):
        """
        queryset filtering for CO owners edit/add: CO user FK
        link: "/mo_admin/company_organisations_companyorganisationowner/<number>/<change/add>"
        """

        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(organization__member_organisation__in=allowed_organizations)
        return queryset

    @classmethod
    def get_company_organisations__companyorganisation_queryset(cls, request, queryset):
        """
        queryset filtering for CO owners edit/add: CO FK
        link: "/mo_admin/company_organisations_companyorganisationowner/<number>/<change/add>"
        """

        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(member_organisation__in=allowed_organizations)
        return queryset


class CompanyOrganisationUserCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX

    @classmethod
    def get_company_organisations__companyorganisationuser_queryset(cls, request, queryset):
        """
        queryset filtering for CO users changelist
        link: "/mo_admin/company_organisations_companyorganisationuser/"
        """

        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(organization__member_organisation__in=allowed_organizations)
        return queryset

    @classmethod
    def get_auth__user_queryset(cls, request, queryset):
        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(
            member_organisations_memberorganisation__in=allowed_organizations
        )
        return queryset

    @classmethod
    def get_company_organisations__companyorganisation_queryset(cls, request, queryset):
        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(member_organisation__in=allowed_organizations)
        return queryset


class PrefixCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX

    @classmethod
    def get_prefixes__prefix_queryset(cls, request, queryset):
        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(member_organisation__in=allowed_organizations)
        return queryset

    @classmethod
    def get_company_organisations__companyorganisation_queryset(cls, request, queryset):
        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(member_organisation__in=allowed_organizations)
        return queryset

    @classmethod
    def get_member_organisations__memberorganisation_queryset(cls, request, queryset):
        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(pk__in=allowed_organizations)
        return queryset


class ProductCustomAdmin(BaseCustomAdminMethods):
    url_prefix = URL_PREFIX

    @classmethod
    def get_products__product_queryset(cls, request, queryset):
        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(
            owner__member_organisations_memberorganisation__in=allowed_organizations
        )
        return queryset

    @classmethod
    def get_auth__user_queryset(cls, request, queryset):
        allowed_organizations = get_allowed_mo_for_mo_admin(request.user)
        queryset = queryset.filter(
            member_organisations_memberorganisation__in=allowed_organizations
        )
        return queryset
