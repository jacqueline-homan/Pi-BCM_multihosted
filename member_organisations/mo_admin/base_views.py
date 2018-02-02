from functools import update_wrapper

import copy
from django.contrib.admin import widgets
from django.db import models
from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.urls import path, reverse


class BaseMOAdmin(admin.ModelAdmin):
    url_prefix = 'mo_admin'
    change_list_template = 'admin/mo_admin/change_list.html'
    change_form_template = 'admin/mo_admin/change_form.html'
    related_models_actions = None

    app_label = None
    model_name = None

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        if not self.related_models_actions:
            self.related_models_actions = dict()

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
            queryset = getattr(self, method_name)(request, queryset)
        else:
            raise NotImplementedError(f'Not implemented "{self}.{method_name}()"')
        return queryset

    # related permissions section start -->
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """
        MO ADMIN NOTE: it's a COPY FROM admin.options.BaseModelAdmin
                       to replace related actions behaviour

        Hook for specifying the form Field instance for a given database Field
        instance.

        If kwargs are given, they're passed to the form Field's constructor.
        """
        # If the field specifies choices, we don't need to look for special
        # admin widgets - we just need to use a select widget of some kind.
        if db_field.choices:
            return self.formfield_for_choice_field(db_field, request, **kwargs)

        # ForeignKey or ManyToManyFields
        if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
            # Combine the field kwargs with any options for formfield_overrides.
            # Make sure the passed in **kwargs override anything in
            # formfield_overrides because **kwargs is more specific, and should
            # always win.
            if db_field.__class__ in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[db_field.__class__], **kwargs)

            # Get the correct formfield.
            if isinstance(db_field, models.ForeignKey):
                formfield = self.formfield_for_foreignkey(db_field, request, **kwargs)
            elif isinstance(db_field, models.ManyToManyField):
                formfield = self.formfield_for_manytomany(db_field, request, **kwargs)

            # For non-raw_id fields, wrap the widget with a wrapper that adds
            # extra HTML -- the "add other" interface -- to the end of the
            # rendered output. formfield can be None if it came from a
            # OneToOneField with parent_link=True or a M2M intermediary.
            if formfield and db_field.name not in self.raw_id_fields:
                related_modeladmin = self.admin_site._registry.get(db_field.remote_field.model)
                wrapper_kwargs = {}
                if related_modeladmin:
                    wrapper_kwargs.update(
                        can_add_related=related_modeladmin.has_add_permission(request),
                        can_change_related=related_modeladmin.has_change_permission(request),
                        can_delete_related=related_modeladmin.has_delete_permission(request),
                    )

                    # MO ADMIN customizations are here
                    if self.related_models_actions.get(db_field.name):
                        wrapper_kwargs = self.related_models_actions.get(db_field.name)
                    else:
                        # disable all related actions if they weren't specified explicitly
                        wrapper_kwargs = {
                            'can_add_related': False,
                            'can_change_related': False,
                            'can_delete_related': False,
                        }

                # MO ADMIN note,
                # this method could be overriden to provide internal urls to related models:
                # RelatedFieldWidgetWrapper.get_related_url()
                formfield.widget = widgets.RelatedFieldWidgetWrapper(
                    formfield.widget, db_field.remote_field, self.admin_site, **wrapper_kwargs
                )

            return formfield

        # If we've got overrides for the formfield defined, use 'em. **kwargs
        # passed to formfield_for_dbfield override the defaults.
        for klass in db_field.__class__.mro():
            if klass in self.formfield_overrides:
                kwargs = dict(copy.deepcopy(self.formfield_overrides[klass]), **kwargs)
                return db_field.formfield(**kwargs)

        # For any other type of field, just call its formfield() method.
        return db_field.formfield(**kwargs)

    # related permissions section end <--

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
