from django import forms
from django.core.validators import validate_email

from member_organisations.models import MemberOrganisation

def get_mo_choices():
    # choices should be specified with method!
    # if you replace "choices" with an internal class member,
    # ChoiceField tests will fail (choices will be empty)
    return [
        (mo.slug.lower(), mo.name) for mo in MemberOrganisation.objects.all()
    ]


class AccountCreateOrUpdateForm(forms.Form):
    uuid = forms.CharField(label='Unique User Id', required=True)
    email = forms.CharField(label='User Email', required=True, validators=[validate_email])
    company_prefix = forms.CharField(label='Company Prefix', required=True)
    company_name = forms.CharField(label='Company Name', required=False)
    credits = forms.CharField(label='Credit Points', required=False)
    txn_ref = forms.CharField(label='Unique Transaction Reference', required=False)
    member_organisation = forms.ChoiceField(label='GS1 MO', choices=get_mo_choices, required=True)
