from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from products.models import Product,Unit


@receiver(pre_delete, sender=Product)
def delete_units(sender, instance, **kwargs):
    pass

@receiver(post_save, sender=Product)
def create_unit(sender, instance, created, **kwargs):
    if created:
        Unit.objects.create(
            name="حبة",
            product=sender,
            conversion_factor=1,

        )