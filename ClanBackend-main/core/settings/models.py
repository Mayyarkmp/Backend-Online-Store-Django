from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from .base import AbstractCity, AbstractCountry, AbstractRegion, AbstractSubRegion
from cities_light.receivers import connect_default_signals


class Country(AbstractCountry):
    is_supported = models.BooleanField(_("Is Supported"), default=True)

    class Meta:
        app_label = "settings"

    def __str__(self):
        return self.name

connect_default_signals(Country)

class Region(AbstractRegion):
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE)
    is_supported = models.BooleanField(_("Is Supported"), default=True)

    class Meta:
        app_label = "settings"

    def __str__(self):
        return f"{self.name}, {self.country.name}"
    
connect_default_signals(Region)


class SubRegion(AbstractRegion):
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE)
    region = models.ForeignKey(Region,
                               null=True, blank=True,
                               on_delete=models.CASCADE)
    is_supported = models.BooleanField(_("Is Supported"), default=True)

    class Meta:
        app_label = "settings"

    def __str__(self):
        return f"{self.name}, {self.country.name}"


connect_default_signals(SubRegion)

class City(AbstractCity):
    subregion = models.ForeignKey(SubRegion,
                                  blank=True, null=True,
                                  on_delete=models.CASCADE)
    region = models.ForeignKey(Region, blank=True,
                               null=True, on_delete=models.CASCADE)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE)
    is_supported = models.BooleanField(_("Is Supported"), default=True)

    class Meta:
        app_label = "settings"

    def __str__(self):
        return f"{self.name}, {self.region.name}, {self.country.name}"

connect_default_signals(City)


# class PaymentService(models.Model):
#     name = models.CharField(_("Payment Service Name"), max_length=100)
#     is_active = models.BooleanField(_("Is Active"), default=True)
    

#     def __str__(self):
#         return self.name