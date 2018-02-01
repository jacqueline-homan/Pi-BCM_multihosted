from functools import update_wrapper

from django.contrib import admin
from django.urls import path, reverse


class BaseMOAdmin(admin.ModelAdmin):
    url_prefix = 'mo_admin'
    change_list_template = 'admin/mo_admin/change_list.html'
    change_form_template = 'admin/mo_admin/change_form.html'
    # exclude = ('username', )  # prevent to view/update "self" fields

    # cached_querysets = None
    app_label = None
    model_name = None

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        # self.cached_querysets = dict()
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = self.filter_queryset_by_permissions(request, queryset=queryset)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        form_field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if not form_field:
            return None

        form_field.queryset = self.filter_queryset_by_permissions(
            request, queryset=form_field.queryset
        )
        return form_field

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
        if not form_field:
            return None

        form_field.queryset = self.filter_queryset_by_permissions(
            request, queryset=form_field.queryset
        )
        return form_field

    def filter_queryset_by_permissions(self, request, queryset):
        method_name = (
            f'get_{queryset.model._meta.app_label}__{queryset.model._meta.model_name}_queryset'
        ).lower()

        if callable(getattr(self, method_name, None)):
            # cached querysets, sometimes django calls this method a few times for the same field
            # if method_name in self.cached_querysets:
            #     return self.cached_querysets[method_name]

            queryset = getattr(self, method_name)(request, queryset)
            # self.cached_querysets[method_name] = queryset
        else:
            raise NotImplementedError(f'Not implemented "{self}.{method_name}()"')
        return queryset

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
        extra_context['mo_admin_changelist_url'] = reverse(
            f'admin:{self.url_prefix}_{self.app_label}_{self.model_name}_changelist'
        )

        if args:
            extra_context['mo_admin_delete_url'] = reverse(
                f'admin:{self.url_prefix}_{self.app_label}_{self.model_name}_delete',
                args=args
            )
        return extra_context

    def mo_admin_changelist_view(self, request, extra_context=None):
        extra_context = self.get_urls_context()
        return super().changelist_view(request, extra_context)

    def mo_admin_add_view(self, request, form_url='', extra_context=None):
        return super().add_view(request, form_url, extra_context)

    def mo_admin_change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = self.get_urls_context(args=(object_id, ))
        return super().change_view(request, object_id, form_url, extra_context)

    def mo_admin_delete_view(self, request, object_id, extra_context=None):
        return super().delete_view(request, object_id, extra_context)
