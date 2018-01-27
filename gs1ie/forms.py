from django import forms
from django.utils.translation import gettext as _

from member_organisations.models import MemberOrganisation

def get_mo_choices():
    # choices should be specified with method!
    # if you replace "choices" with an internal class member,
    # ChoiceField tests will fail (choices will be empty)
    return [
        (mo.slug.lower(), mo.name) for mo in MemberOrganisation.objects.all()
    ]


class AccountCreateOrUpdateForm(forms.Form):
    uuid = forms.CharField(label=_('Unique User Id'))
    email = forms.EmailField(label=_('User Email'))
    company_prefix = forms.CharField(label=_('Company Prefix'))
    company_name = forms.CharField(label=_('Company Name'), required=False)
    credits = forms.CharField(label=_('Credit Points'), required=False)
    txn_ref = forms.CharField(
        label=_('Unique Transaction Reference'), required=False)
    member_organisation = forms.ChoiceField(
        label=_('GS1 MO'), choices=get_mo_choices)
