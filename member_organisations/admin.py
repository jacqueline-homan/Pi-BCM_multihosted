from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path, reverse, NoReverseMatch

from member_organisations.models import (
    MemberOrganisation, MemberOrganisationOwner, MemberOrganisationUser
)

from .mo_admin.apps_config import apps_config as mo_apps_config
from .go_admin.apps_config import apps_config as go_apps_config


class MemberOrganisationOwnerAdmin(admin.ModelAdmin):
    list_display = ('organization_user', 'organization')

    # configuration ordered dicts
    mo_apps = mo_apps_config
    go_apps = go_apps_config

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('mo_admin/', self.mo_admin_index, name='mo_admin'),
            path('go_admin/', self.go_admin_index, name='go_admin'),
        ]

        # retrieving custom urls for all apps and all required models (go admin)
        custom_urls += self.get_custom_urls_for_config(self.go_apps)
        # retrieving custom urls for all apps and all required models (mo admin)
        custom_urls += self.get_custom_urls_for_config(self.mo_apps)

        return custom_urls + urls  # urls order matters!

    @classmethod
    def get_custom_urls_for_config(cls, apps_config):
        """
        Retrieving custom urls for all apps and all required models go admin
        """

        custom_urls = list()
        for app_label, admin_views in apps_config.items():
            for admin_view in admin_views:
                custom_urls += admin_view.get_custom_urls()

        return custom_urls

    @classmethod
    def get_reverse_url(cls, url_prefix, app_label, model_name, action, default=''):
        try:
            return reverse(f'admin:{url_prefix}_{app_label}_{model_name}_{action}')
        except NoReverseMatch:
            return default

    def get_app_list(self, request, apps_config, url_prefix):
        """
        Retrieves allowed app list, update urls to custom admin views
        """

        app_list = [
            item for item in self.admin_site.get_app_list(request)
            if item.get('app_label') in apps_config.keys()
        ]

        for app in app_list:
            app_label = app.get('app_label', '')
            app['app_url'] = '#'  # prevent direct urls to base django admin
            for model in app.get('models', []):
                model_name = model.get('object_name', '').lower()

                model['admin_url'] = self.get_reverse_url(
                    url_prefix, app_label, model_name, action='changelist'
                )
                model['add_url'] = self.get_reverse_url(
                    url_prefix, app_label, model_name, action='add'
                )

        return app_list

    def mo_admin_index(self, request):
        """
        index page for mo admin, displays list of required apps
        :param request:
        :return:
        """

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            app_list=self.get_app_list(request, self.mo_apps, url_prefix='mo_admin'),
        )
        return TemplateResponse(request, 'admin/mo_admin/index.html', context)

    def go_admin_index(self, request):
        """
        index page for mo admin, displays list of required apps
        :param request:
        :return:
        """

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            app_list=self.get_app_list(request, self.go_apps, url_prefix='go_admin'),
        )
        return TemplateResponse(request, 'admin/go_admin/index.html', context)


class MemberOrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'slug')


class MemberOrganisationUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'is_admin')


admin.site.register(MemberOrganisationOwner, MemberOrganisationOwnerAdmin)
admin.site.register(MemberOrganisation, MemberOrganisationAdmin)
admin.site.register(MemberOrganisationUser, MemberOrganisationUserAdmin)
