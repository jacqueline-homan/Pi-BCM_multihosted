# Deprecated. Language switch came from middleware.

import django.utils.translation as trans
from BCM.models import LanguageByCountry, Language


def switch_language(request, language_slug):
    trans.activate(language_slug)
    request.session[trans.LANGUAGE_SESSION_KEY] = language_slug


def _set_default_language_by_country(request, country_slug):
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
            # fallback to default
            language_slug = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')

        switch_language(request, language_slug)
        return True

    return False


def _set_language_by_user(request):
    if request.user.is_authenticated:
        language_slug = request.user.profile.language.slug
        if not language_slug:
            # fallback to default
            language_slug = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')

        switch_language(request, language_slug)
        return True

    return False


def set_language_by_country(view_func, *args, **kwargs):
    def decorator(request, *dargs, **dkwargs):
        """
        request and country code parameters are expected
        """

        country_slug = dkwargs.get('country', '') or None
        _set_default_language_by_country(request, country_slug)
        return view_func(request, *dargs, **dkwargs)
    return decorator


def set_language_by_user(view_func, *args, **kwargs):
    def decorator(request, *dargs, **dkwargs):
        """
        request parameter is expected
        """
        _set_language_by_user(request)
        return view_func(request, *dargs, **dkwargs)

    return decorator


def set_language_by_auto(view_func, *args, **kwargs):
    def decorator(request, *dargs, **dkwargs):
        """
        tries to set language by user, if not succeeded, by country
        """

        language_is_set = False

        if request.GET.get('new_language'):
            language_slug = request.GET.get('new_language')
            if Language.objects.filter(slug__iexact=language_slug):
                switch_language(request, language_slug)
                language_is_set = True

        if not language_is_set:
            country_slug = dkwargs.get('country', '') or None
            language_is_set = _set_default_language_by_country(request, country_slug)

        if not language_is_set:
            _set_language_by_user(request)

        return view_func(request, *dargs, **dkwargs)

    return decorator
