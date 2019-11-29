
# Django Library
from eatple_app.models import Store, Menu
from eatple_app.models import Category, Tag
from eatple_app.models import Order
from django.urls import reverse
from django.db import models
from django_mysql.models import Model

# External Library

# Define
from eatple_app.define import *

class Partner(models.Model):
    class Meta:
        ordering = ['-storeInstance__name']

    name = models.CharField(max_length=PARTNER_ID_CODE_LENGTH,
                            help_text="Partner Name", default='')
    storeInstance = models.ForeignKey(
        'Store', on_delete=models.CASCADE, default=DEFAULT_OBJECT_ID)
    identifier_code = models.CharField(
        max_length=PARTNER_ID_CODE_LENGTH, help_text="Partner ID", default='')

    @classmethod
    def registerPartner(cls, _name, _identifier_code, _storeKey):
        try:
            storeInstance = Store.objects.get(id=_storeKey)
        except Store.DoesNotExist:
            return None

        registedUser = cls(
            name=_name, identifier_code=_identifier_code, storeInstance=storeInstance)
        registedUser.save()

        return registedUser

        # Methods
    def __str__(self):
        return "{} : {}".format(self.name, self.storeInstance.name)
