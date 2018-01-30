from .models import Language, LanguageByCountry


def add_languages(request):
    context_data = {}
    if request.user.is_authenticated:
        try:
            user_country = request.user.profile.country
            language_by_country = LanguageByCountry.objects.filter(
                country=user_country)
            languages = [x.language for x in language_by_country]
        except AttributeError:
            languages = Language.objects.all()  # GO admin might not have MO set, so no country
    else:
        languages = Language.objects.all()
    context_data["languages"] = languages
    return context_data
