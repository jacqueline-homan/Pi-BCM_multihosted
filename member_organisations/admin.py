from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path, reverse, NoReverseMatch

from .models import MemberOrganisation, MemberOrganisationOwner, MemberOrganisationUser

from .mo_admin.audit_views import AuditLogAdmin
from audit.models import Log

audit_mo_admin = AuditLogAdmin(Log, admin.site)


class MemberOrganisationOwnerAdmin(admin.ModelAdmin):
    allowed_app_labels = (
        'company_organisations',
        'prefixes',
        'products',
        'audit',
    )

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path('mo_admin/', self.admin_site.admin_view(self.mo_admin_index), name='mo_admin'),
        ]
        audit_custom_urls = audit_mo_admin.get_custom_urls()  # repeat for each model
        all_urls = custom_urls + audit_custom_urls + urls  # urls order matters!
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
            if item.get('app_label') in self.allowed_app_labels
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
