from collections import OrderedDict

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path, reverse, NoReverseMatch

from audit.models import Log
from company_organisations.models import (
    CompanyOrganisation, CompanyOrganisationOwner, CompanyOrganisationUser
)
from prefixes.models import Prefix
from products.models import Product
from member_organisations.models import (
    MemberOrganisation, MemberOrganisationOwner, MemberOrganisationUser
)

from .mo_admin.mo_views import (
    AuditLogMOAdmin, CompanyOrganisationMOAdmin, CompanyOrganisationOwnerMOAdmin,
    CompanyOrganisationUserMOAdmin, PrefixMOAdmin, ProductMOAdmin
)


class MemberOrganisationOwnerAdmin(admin.ModelAdmin):
    mo_apps = OrderedDict([
        ('audit', [
            AuditLogMOAdmin(Log, admin.site)
        ]),
        ('company_organisations', [
            CompanyOrganisationMOAdmin(CompanyOrganisation, admin.site),
            CompanyOrganisationOwnerMOAdmin(CompanyOrganisationOwner, admin.site),
            CompanyOrganisationUserMOAdmin(CompanyOrganisationUser, admin.site),
        ]),
        ('prefixes', [
            PrefixMOAdmin(Prefix, admin.site)
        ]),
        ('products', [
            ProductMOAdmin(Product, admin.site)
        ]),
    ])

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('mo_admin/', self.admin_site.admin_view(self.mo_admin_index), name='mo_admin'),
        ]

        # audit_custom_urls = audit_mo_admin.get_custom_urls()  # repeat for each model
        for app_label, admin_views in self.mo_apps.items():
            for admin_view in admin_views:
                custom_urls += admin_view.get_custom_urls()

        all_urls = custom_urls + urls  # urls order matters!
        return all_urls

    @classmethod
    def get_reverse_url(cls, app_label, model_name, action, default=''):
        try:
            return reverse(f'admin:mo_admin_{app_label}_{model_name}_{action}')
        except NoReverseMatch:
            return default

    def get_app_list(self, request):
        """
        Retrieves allowed app list, update urls to mo_admin views
        :param request:
        :return:
        """

        app_list = [
            item for item in self.admin_site.get_app_list(request)
            if item.get('app_label') in self.mo_apps.keys()
        ]

        for app in app_list:
            app_label = app.get('app_label', '').lower()
            app['app_url'] = '#'  # prevent direct urls to base django admin
            for model in app.get('models', []):
                model_name = model.get('object_name', '').lower()

                model['admin_url'] = self.get_reverse_url(
                    app_label, model_name, action='changelist'
                )
                model['add_url'] = self.get_reverse_url(
                    app_label, model_name, action='add'
                )

        return app_list

    def mo_admin_index(self, request):
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            app_list=self.get_app_list(request),
        )

        return TemplateResponse(request, 'admin/mo_admin/index.html', context)


admin.site.register(MemberOrganisation)
admin.site.register(MemberOrganisationOwner, MemberOrganisationOwnerAdmin)
admin.site.register(MemberOrganisationUser)
