from django import forms
from django.core.validators import validate_email


class AccountCreateOrUpdateForm(forms.Form):
    uuid           = forms.CharField(label='Unique User Id', required=True)
    email          = forms.CharField(label='User Email',     required=True, validators=[validate_email])
    company_prefix = forms.CharField(label='Company Prefix', required=True)
    company_name   = forms.CharField(label='Company Name',   required=False)
    credits        = forms.CharField(label='Credit Points',  required=False)
    txn_ref        = forms.CharField(label='Unique Transaction Reference', required=False)
