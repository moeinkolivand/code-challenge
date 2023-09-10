from django.db import models
from django.utils.translation import gettext_lazy as _


class GENDER(models.IntegerChoices):
    MALE = 0, _("male")
    FEMALE = 1, _("female")
