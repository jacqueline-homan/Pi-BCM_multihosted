from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row

register = template.Library()


@register.inclusion_tag('admin/mo_admin/submit_line.html', takes_context=True)
def mo_admin_submit_row(context):
    """
    Override submit row to specify required mo_admin template
    """

    return submit_row(context)
