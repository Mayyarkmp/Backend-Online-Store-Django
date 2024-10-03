from django.contrib.gis.db import models


class Role(models.Model):
    class Types(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        STAFF = 'STAFF', 'Staff'
        DELIVERY = 'DELIVERY', 'Delivery'
        PREPARER = 'PREPARER', 'Preparer'

    type = models.CharField(max_length=20, choices=Types.choices)
    permissions = models.ManyToManyField('branches.Permission', related_name='roles')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Permission(models.Model):
    class Levels(models.TextChoices):
        ALL = 'ALL', 'All'
        OWNER = 'OWNER', 'Owner'

    class Types(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        STAFF = 'STAFF', 'Staff'
        DELIVERY = 'DELIVERY', 'Delivery'
        PREPARER = 'PREPARER', 'Preparer'

    level = models.CharField(max_length=20, choices=Levels.choices)
    type = models.CharField(max_length=20, choices=Types.choices)
    name = models.CharField(max_length=50, null=True, blank=True)
    codename = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name or self.codename
