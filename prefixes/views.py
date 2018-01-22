from django.shortcuts import render
from django.conf import settings


def prefixes(request):
    config = { 'GS1_GLN_CAPABILITY': settings.GS1_GLN_CAPABILITY }

    context = {
        'config': config
    }
    return render(request, 'prefixes/prefixes_list.html', context)
