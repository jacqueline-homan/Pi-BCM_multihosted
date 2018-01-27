from django.shortcuts import render, redirect, reverse
from . import models
import django.utils.translation as trans
from django.contrib.auth import views as auth_views
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.


def set_language(lang, request):
    trans.activate(lang)
    request.session[trans.LANGUAGE_SESSION_KEY] = lang


def set_language_by_country(request, country):

    selected_lang = models.LanguageByCountry.objects.filter(
        country__slug=country, default=True).first()
    if selected_lang is None:
        selected_lang = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')
    else:
        selected_lang = selected_lang.language.slug
    if request.method == "POST":
        selected_lang = request.POST.get("language", selected_lang)
    set_language(selected_lang, request)


def set_language_by_user(request, country):
    user = request.user
    if user.is_authenticated:
        lang = user.profile.language
        if lang:
            set_language(lang.slug, request)
            return
        else:
            country = user.profile.country
            if country:
                set_language_by_country(request, country.slug)
                return
        set_language_by_country(request, country)


def index_redirect(request):
    country = "__"
    if request.method == "POST":
        country = request.POST.get("country")
        country_obj = models.Country.objects.filter(slug=country).first()
        lang = country_obj.get_default_language()
        set_language(lang.language.slug, request)
        return redirect(reverse('index', args=[country]))
    else:
        countries = models.Country.objects.all()
    return render(request, "generic.html", {"countries": countries, "country": country })


def index(request, country):
    langs = models.LanguageByCountry.objects.filter(country__slug=country)
    set_language_by_country(request, country)
    return render(request, 'index.html', {"languages": langs, "country": country})


@login_required
def after_login(request, country):
    set_language_by_user(request, country)
    return redirect("profile", pk=request.user.username, country=country)


class CountryLogin(auth_views.LoginView):

    def dispatch(self, request, *args, **kwargs):
        self.country = kwargs.get("country")
        return super(CountryLogin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["country"] = self.country
        context["next"] = "after_login"
        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    model = models.Profile
    template_name = "profile.html"
    fields = ["country", "language"]
    success_url = "profile"

    def dispatch(self, request, *args, **kwargs):
        self.country = kwargs.get("country")
        self.username = request.user.username
        set_language_by_user(request, self.country)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["country"] = self.country
        return context


class RegisterUser(CreateView):
    model = User
    template_name = "registration/registration.html"
    form = UserCreationForm
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        self.country = kwargs.get("country")
        self.request = request
        set_language_by_country(request, self.country)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["country"] = self.country
        return context

    def get_form_class(self):
        return UserCreationForm

    def get_success_url(self):
        self.username = self.object.username
        login(self.request, self.object)
        return reverse("profile", args=(self.country, self.object.username))
