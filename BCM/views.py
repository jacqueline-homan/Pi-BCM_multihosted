from django.shortcuts import render, redirect, reverse
from . import models
import django.utils.translation as trans
# Create your views here.


def index_redirect(request):
    if request.method == "POST":
        country = request.POST.get("country")
        country_obj = models.Country.objects.filter(slug=country).first()
        lang = country_obj.get_default_language()
        trans.activate(lang.language.slug)
        request.session[trans.LANGUAGE_SESSION_KEY] = lang.language.slug
        return redirect(reverse('index', args=[country]))
    else:
        countries = models.Country.objects.all()
    return render(request, "generic.html", {"countries": countries})


def index(request, country):
    langs = models.LanguageByCountry.objects.filter(country__slug=country)
    if request.method == "POST":
        default_lang = models.LanguageByCountry.objects.filter(country__slug=country, default=True)
        selected_lang = request.POST.get("language", default_lang)
    return render(request, 'index.html', {"languages": langs})
