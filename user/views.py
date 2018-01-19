from django.shortcuts import render
from django.shortcuts import render


def profile(request):
    context = {}
    return render(request, 'user/profile.html', context)
