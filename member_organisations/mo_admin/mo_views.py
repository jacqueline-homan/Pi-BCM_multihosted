from functools import update_wrapper

from django.core.exceptions import PermissionDenied
from django.contrib import admin
from django.urls import path, reverse

from company_organisations.models import CompanyOrganisationOwner
from member_organisations.models import MemberOrganisationOwner
from .base_views import BaseMOAdmin


class AuditLogMOAdmin(BaseMOAdmin):
    @classmethod
    def get_audit__log_queryset(cls, request, queryset):
        # todo: there are no fields to filter this model!
        return queryset


class CompanyOrganisationMOAdmin(BaseMOAdmin):
    exclude = ('member_organisation', )

    @classmethod
    def get_company_organisations__companyorganisation_queryset(cls, request, queryset):
        """
        name convention:
            "get_{model._meta.app_label}__{model._meta.model_name}_queryset".lower()
        """

        member_organization_admin_ids = (  # mo where the current user is admin
            request.user.member_organisations_memberorganisationuser
            .filter(is_admin=True)
            .values_list('organization', flat=True)
        )
        member_organization_owner_ids = (  # mo where the current user is owner
            MemberOrganisationOwner.objects
            .filter(organization__owner__organization_user__user=request.user)
            .values_list('organization', flat=True)
        )
        allowed_organizations = (
                set(member_organization_admin_ids) | set(member_organization_owner_ids)
        )
        queryset = queryset.filter(member_organisation__in=allowed_organizations)
        return queryset

    @classmethod
    def get_bcm__country_queryset(cls, request, queryset):
        return queryset


class CompanyOrganisationOwnerMOAdmin(BaseMOAdmin):
    @classmethod
    def get_company_organisations__companyorganisationowner_queryset(cls, request, queryset):

        # 1. filter by organization, company organization should belong to request.user MO
        # 2. filter by user, organization user should belong to CO, which belong to request.user MO

        return queryset


class CompanyOrganisationUserMOAdmin(BaseMOAdmin):
    pass


class PrefixMOAdmin(BaseMOAdmin):
    pass


class ProductMOAdmin(BaseMOAdmin):
    pass
