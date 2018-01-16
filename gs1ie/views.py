from django.shortcuts import render
from .forms import AccountCreateOrUpdateForm
from uam.models import organisation_service
from user.models import users_service


class User:
    def is_authenticated(self):
        return True


def account_create_or_update(request):
    if request.method == 'POST':
        form = AccountCreateOrUpdateForm(request.POST)
        if form.is_valid():
            try:
                # core data
                email = form.data.get('email')
                company = form.data.get('company_name')

                # get company
                organisation, organisation_created = organisation_service.get_or_create(uuid=form.data.get('uuid'))

                # update company name if any
                if company:
                    organisation_service.update(organisation, company=company)

                # get or create user
                user, user_created = users_service.get_or_create(email=email,
                                                                 defaults={
                                                                     'username': email,
                                                                     'customer_role': 'gs1ie',
                                                                     'organisation': organisation
                                                                 })
            except Exception as e:
                print(e)
            form = AccountCreateOrUpdateForm()
    else:
        form = AccountCreateOrUpdateForm()

    current_user = User()
    context = { 'current_user': current_user,
                'active_page': '',
                'form': form }
    return render(request, 'gs1ie/AccountCreateOrUpdate.html', context)
