# we use 100 characters line length, isn't it?
from django.shortcuts import render, redirect, reverse

# from BCM.decorators import set_language_by_country, set_language_by_user, set_language_by_auto
from . import models
# import django.utils.translation as trans
from django.contrib.auth import views as auth_views
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
# from django.utils.decorators import method_decorator


# @set_language_by_auto
def index_redirect(request):
    # country = "__"
    # if request.method == "POST":
    #     country = request.POST.get("country")
    #     country_obj = models.Country.objects.filter(slug=country).first()
    #     # lang = country_obj.get_default_language()
    #     # set_language(lang.language.slug, request)
    #     return redirect(reverse('index', args=[country]))
    # else:
    #     countries = models.Country.objects.all()

    countries = models.Country.objects.all()
    return render(request, "bcm/generic.html", {"countries": countries})


# @set_language_by_auto
def index(request, country):
    # langs = models.LanguageByCountry.objects.filter(country__slug=country)
    # set_language_by_country(request, country)
    countries = models.Country.objects.all()
    return render(request, 'bcm/generic.html', {"countries": countries})

@login_required
# @set_language_by_auto
def after_login(request, country):
    # set_language_by_user(request, country)
    return redirect("profile", pk=request.user.username, country=country)

class CountryLogin(auth_views.LoginView):
    template_name = 'bcm/registration/login.html'

    # @method_decorator(set_language_by_auto)
    def dispatch(self, request, *args, **kwargs):
        self.country = kwargs.get("country")
        return super(CountryLogin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["country"] = self.country
        context["next"] = "after_login"
        return context

'''
class ProfileView(LoginRequiredMixin, UpdateView):
    model = models.Profile
    template_name = "bcm/profile.html"
    fields = ["country", "language"]
    success_url = "profile"

    # @method_decorator(set_language_by_auto)
    def dispatch(self, request, *args, **kwargs):
        # self.country = kwargs.get("country")
        self.username = request.user.username
        # set_language_by_user(request, self.country)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["country"] = self.country
        return context
'''

class RegisterUser(CreateView):
    model = User
    template_name = "bcm/registration/registration.html"
    form = UserCreationForm
    fields = "__all__"

    # @method_decorator(set_language_by_country)
    def dispatch(self, request, *args, **kwargs):
        self.country = kwargs.get("country")
        # self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["country"] = self.country
        return context

    def get_form_class(self):
        return UserCreationForm

    def get_success_url(self):
        self.username = self.object.username
        login(self.request, self.object)
        return reverse("profile", args=(self.country, self.object.username))
