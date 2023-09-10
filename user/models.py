from django.db import models
from django.utils.translation import gettext_lazy as _
from tethercodereview.models import BaseModel
from django.contrib.auth.models import AbstractUser
from user.managers import CustomUserManager
from user.enums import GENDER
from user.validators import is_valid_phone_number
from django.core.exceptions import ValidationError


class BaseUser(AbstractUser, BaseModel):
    phone_number = models.CharField(
        max_length=11, unique=True, verbose_name="Phone Number"
    )
    objects = CustomUserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    username = None
    is_authenticated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number if self.get_full_name() == "" else self.get_full_name()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class UserInformation(BaseModel):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, verbose_name="User")
    national_card = models.ImageField(upload_to="nationalcard", blank=True)
    bank_card = models.CharField(max_length=16, verbose_name="Bank Card Number")
    gender = models.IntegerField(default=GENDER.MALE, choices=GENDER.choices)
    recognizance = models.ImageField(upload_to="recognizance", blank=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "UserInformation"
        verbose_name_plural = "UserInformations"


class User(BaseUser):
    objects = CustomUserManager()

    def clean(self):
        if not is_valid_phone_number(self.phone_number):
            raise ValidationError(
                _("%(value)s is not correct phone number format"),
                params={"value": self.phone_number},
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(BaseUser, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    class Meta:
        proxy = True
