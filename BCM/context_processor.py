from .models import Language


def add_languages(request):
    context_data = {}
    context_data["languages"] = Language.objects.all()
    return context_data
