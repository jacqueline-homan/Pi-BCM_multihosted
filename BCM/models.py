from django.db import models
import random
# from organizations.models import
# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=2)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return "{} ({})".format(self.name, self.slug)

    def get_default_language(self):
    	default_lang = LanguageByCountry.objects.filter(country=self, default=True).first()
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
        verbose_name_plural = "Languages by countries"

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
