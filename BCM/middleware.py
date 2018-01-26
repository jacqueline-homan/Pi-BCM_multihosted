import django.utils.translation as trans
from .models import LanguageByCountry


class LanguageSwitcher:

    def set_language(self, request, *dargs, **dkwargs):
        """
        hierarchy:
        - GET parameter "new_language"
        - stored in "pref_language" per user sessions
        - authenticated user preferred language
        - country default language
        - HTTP_ACCEPT_LANGUAGE
        - English
        """

        language_slug = request.GET.get('new_language')

        if not language_slug:
            language_slug = request.session.get("pref_language")
        else:
            request.session["pref_language"] = language_slug

        if not language_slug and request.user.is_authenticated:
            try:
                language_slug = request.user.profile.language.slug
            except Exception as e:
                language_slug = None

        if not language_slug:
            country_slug = dkwargs.get('country')
            if country_slug:
                try:
                    language_by_country = LanguageByCountry.objects.get(
                        country__slug__iexact=country_slug, default=True
                    )
                except (LanguageByCountry.DoesNotExist, LanguageByCountry.MultipleObjectsReturned):
                    language_slug = None
                else:
                    language_slug = language_by_country.language.slug

        if not language_slug:
            language_slug = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')

        trans.activate(language_slug)
        request.session[trans.LANGUAGE_SESSION_KEY] = language_slug

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, views_args, view_kwargs):
        self.set_language(request, **view_kwargs)
        return None
