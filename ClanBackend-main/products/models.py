import uuid

from django.db import models
from parler.models import TranslatedFields

from core.media.models import Media
from core.base.models import TimeStampedTranslatableModel

from django.utils.translation import gettext_lazy as _

class Group(TimeStampedTranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name"),max_length=100)
    )

    products = models.ManyToManyField('Product', related_name='groups', blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    images = models.ManyToManyField(Media, related_name='groups', blank=True)

    def __str__(self):
        return self.name


class Supplier(TimeStampedTranslatableModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    translations = TranslatedFields(
        name=models.CharField(_("Name"),max_length=100)
    )
    images = models.ManyToManyField(Media, verbose_name="Images", blank=True, related_name='suppliers')
    categories = models.ManyToManyField('Category', verbose_name=_("Categories"), related_name='suppliers', blank=True)
    groups = models.ManyToManyField("Group", verbose_name=_("Groups"), related_name='suppliers', blank=True)

    def __str__(self):
        return self.name


class Category(TimeStampedTranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=100)
    )
    image = models.ForeignKey(Media, null=True, blank=True, verbose_name=_("Images"), on_delete=models.SET_NULL, related_name='categories')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=_("Main Category"), on_delete=models.SET_NULL, related_name='children')

    def __str__(self):
        return self.name


class Product(TimeStampedTranslatableModel):

    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=100),
        description=models.TextField(_("Description"),)
    )

    category = models.ForeignKey(Category, verbose_name=_("Category"),on_delete=models.CASCADE, related_name='products')
    supplier = models.ForeignKey(Supplier, verbose_name=_("Supplier"), on_delete=models.CASCADE, related_name='products')
    barcodes = models.ManyToManyField('Barcode', verbose_name=_("Barcodes"), blank=True, related_name='products')
    images = models.ManyToManyField(Media, verbose_name=_("Images"), blank=True, related_name='products')

    def __str__(self):
        return self.name


class TypeUnit(TimeStampedTranslatableModel):

    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=100)
    )

    def __str__(self):
        return self.name


class Unit(TimeStampedTranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=100)
    )
    product = models.ForeignKey(Product, verbose_name=_("Product") ,on_delete=models.CASCADE)
    conversion_factor = models.DecimalField(_("Conversion factor"), max_digits=10, decimal_places=2)
    is_factor = models.BooleanField(_("Is Factor"), default=False)
    is_for_sale = models.BooleanField(_("Is For Sale"), default=False)

    def __str__(self):
        return self.name


class Barcode(TimeStampedTranslatableModel):
    barcode = models.BigIntegerField(_("Barcode"),)

    def __str__(self):
        return self.barcode
