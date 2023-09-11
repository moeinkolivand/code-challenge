from django.db import models
from django.utils.translation import gettext_lazy as _


class PAYMENTSTATUS(models.IntegerChoices):
    NOT_TRANSFERRED = 0, _("NOT TRANSFERRED")
    TRANSFERRED = 1, _("TRANSFERRED")


class TRANSACTIONSTATUS(models.IntegerChoices):
    UNPAID = 0, _("Un Paid")
    PAID = 1, _("Paid")
