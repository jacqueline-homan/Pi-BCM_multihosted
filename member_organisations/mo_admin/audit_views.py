from functools import update_wrapper

from django.contrib import admin
from django.urls import path, include, reverse


class AuditLogAdmin(admin.ModelAdmin):
    url_prefix = 'mo_admin'
    change_list_template = 'admin/mo_admin/change_list.html'
    change_form_template = 'admin/mo_admin/change_form.html'
    exclude = ('username', )  # prevent to view/update "self" fields

    app_label = None
    model_name = None

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    def get_changelist(self, request, **kwargs):
        from member_organisations.mo_admin.change_list import MOAdminChangeList
        return MOAdminChangeList

    def get_custom_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        app_label = self.app_label
        model_name = self.model_name

        custom_urls = [
            path(
                f'{self.url_prefix}/{app_label}_{model_name}/',
                wrap(self.mo_admin_changelist_view),
                name=f'{self.url_prefix}_{app_label}_{model_name}_changelist'
            ),
            path(
                f'{self.url_prefix}/{app_label}_{model_name}/add/',
                wrap(self.mo_admin_add_view),
                name=f'{self.url_prefix}_{app_label}_{model_name}_add',
            ),
            path(
                f'{self.url_prefix}/{app_label}_{model_name}/<path:object_id>/change/',
                wrap(self.mo_admin_change_view),
                name=f'{self.url_prefix}_{app_label}_{model_name}_change',
            ),
            path(
                f'{self.url_prefix}/{app_label}_{model_name}/<path:object_id>/delete/',
                wrap(self.mo_admin_delete_view),
                name=f'{self.url_prefix}_{app_label}_{model_name}_delete',
            ),
        ]

        return custom_urls

    def get_urls_context(self, args=None):
        extra_context = dict()
        extra_context['mo_admin_add_url'] = reverse(
            f'admin:{self.url_prefix}_{self.app_label}_{self.model_name}_add'
        )

        if args:
            extra_context['mo_admin_delete_url'] = reverse(
                f'admin:{self.url_prefix}_{self.app_label}_{self.model_name}_delete',
                args=args
            )
        return extra_context

    def mo_admin_changelist_view(self, request, extra_context=None):
        extra_context = self.get_urls_context()
        response = super().changelist_view(request, extra_context)
        return response

    def mo_admin_add_view(self, request, form_url='', extra_context=None):
        response = super().add_view(request, form_url, extra_context)
        return response

    def mo_admin_change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = self.get_urls_context(args=(object_id, ))
        response = super().change_view(request, object_id, form_url, extra_context)
        return response

    def mo_admin_delete_view(self, request, object_id, extra_context=None):
        response = super().delete_view(request, object_id, extra_context)
        return response

