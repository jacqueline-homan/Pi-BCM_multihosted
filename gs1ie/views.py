from django.shortcuts import render
from .forms import AccountCreateOrUpdateForm


class User:
    def is_authenticated(self):
        return True


def account_create_or_update(request):
    if request.method == 'POST':
        form = AccountCreateOrUpdateForm(request.POST)
        if form.is_valid():
            pass
            form = AccountCreateOrUpdateForm()
    else:
        form = AccountCreateOrUpdateForm()

    current_user = User()
    context = { 'current_user': current_user,
                'active_page': '',
                'form': form }
    return render(request, 'gs1ie/AccountCreateOrUpdate.html', context)

