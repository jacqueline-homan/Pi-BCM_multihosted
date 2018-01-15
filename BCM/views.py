from django.shortcuts import render, redirect, reverse
from . import models
import django.utils.translation as trans
# Create your views here.


def set_language(lang, request):
    trans.activate(lang)
    request.session[trans.LANGUAGE_SESSION_KEY] = lang


def index_redirect(request):
    if request.method == "POST":
        country = request.POST.get("country")
        country_obj = models.Country.objects.filter(slug=country).first()
        lang = country_obj.get_default_language()
        set_language(lang.language.slug, request)
        return redirect(reverse('index', args=[country]))
    else:
        countries = models.Country.objects.all()
    return render(request, "generic.html", {"countries": countries})


def index(request, country):
    langs = models.LanguageByCountry.objects.filter(country__slug=country)
    selected_lang = models.LanguageByCountry.objects.filter(
        country__slug=country, default=True).first()
    if selected_lang is None:
        selected_lang = request.META.get('HTTP_ACCEPT_LANGUAGE','en')
    else:
        selected_lang = selected_lang.language.slug
    if request.method == "POST":
        selected_lang = request.POST.get("language", selected_lang)
    set_language(selected_lang, request)
    return render(request, 'index.html', {"languages": langs})
