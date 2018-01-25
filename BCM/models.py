from django.db import models
import random
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.SlugField(primary_key=True)
    # other info like firstname, surname and other stuff
    country = models.ForeignKey("Country", on_delete=models.CASCADE, null=True)  # ?
    language = models.ForeignKey("Language", on_delete=models.CASCADE, null=True)  # ?

    class Meta:
        verbose_name_plural = _("User profiles")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username)



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    profile_exist = Profile.objects.filter(user=instance).first()
    if profile_exist:
        instance.profile.save()
    else:
        kwargs.pop("created")
        create_user_profile(sender, instance, created=True, **kwargs)


class Country(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=2)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = _("Countries")

    def __str__(self):
        return "{} ({})".format(self.name, self.slug)

    def get_default_language(self):
        default_lang = LanguageByCountry.objects.filter(
            country=self, default=True).first()
        if default_lang:
            return default_lang
        else:
            return random.choice(LanguageByCountry.objects.filter(country=self))


class Language(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=2)

    def __str__(self):
        return "{} ({})".format(self.name, self.slug)


class LanguageByCountry(models.Model):
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    language = models.ForeignKey("Language", on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _("Languages by countries")

    def __str__(self):
        return "{}_{}".format(self.country.slug, self.language.slug)

    def save(self):
        if self.default:
            queryset = LanguageByCountry.objects.filter(
                country=self.country, default=True).exclude(id=self.id).all()
            for record in queryset:
                record.default = False
                record.save()
        super(LanguageByCountry, self).save()
