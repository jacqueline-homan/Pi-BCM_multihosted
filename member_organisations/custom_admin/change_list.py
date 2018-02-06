from django.contrib.admin.views.main import ChangeList
from django.urls import reverse
from django.contrib.admin.utils import quote


class CustomAdminChangeList(ChangeList):
    url_prefix = '__MUST_BE_OVERRIDDEN_AFTER_IMPORT__'

    def __init__(self, request, model, list_display, list_display_links, list_filter,
                 date_hierarchy, search_fields, list_select_related, list_per_page,
                 list_max_show_all, list_editable, model_admin):
        super().__init__(request, model, list_display, list_display_links, list_filter,
                         date_hierarchy, search_fields, list_select_related, list_per_page,
                         list_max_show_all, list_editable, model_admin)

    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)

        return reverse('admin:%s_%s_%s_change' % (self.url_prefix,
                                                  self.opts.app_label,
                                                  self.opts.model_name),
                       args=(quote(pk),),
                       current_app=self.model_admin.admin_site.name)
