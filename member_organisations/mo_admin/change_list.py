from django.contrib.admin.views.main import ChangeList
from django.urls import reverse
from django.contrib.admin.utils import quote


class MOAdminChangeList(ChangeList):
    url_prefix = 'mo_admin'

    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)

        return reverse('admin:%s_%s_%s_change' % (self.url_prefix,
                                                  self.opts.app_label,
                                                  self.opts.model_name),
                       args=(quote(pk),),
                       current_app=self.model_admin.admin_site.name)
