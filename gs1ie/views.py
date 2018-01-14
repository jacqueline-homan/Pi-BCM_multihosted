from django.shortcuts import render
from django.http import HttpResponse

class User:
    def is_authenticated(self):
        return True


def account_create_or_update(request):
    current_user = User()
    context = { 'current_user' : current_user,
                'active_page' : '', }
    return render(request, 'gs1ie/AccountCreateOrUpdate.html', context)

