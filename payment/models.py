from django.contrib.auth import get_user_model
from django.db import models
from payment.enums import PAYMENTSTATUS, GATESTATUS
from currency.models import Currency
from tethercodereview.models import BaseModel


User = get_user_model()


class Payment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    currency = models.OneToOneField(
        Currency, on_delete=models.SET_NULL, null=True, verbose_name="Currency"
    )
    quantity = models.BigIntegerField(verbose_name="quantity")
    status = models.SmallIntegerField(
        choices=PAYMENTSTATUS.choices, default=PAYMENTSTATUS.NOT_TRANSFERRED
    )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class TRANSACTION(BaseModel):
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, verbose_name="Currency"
    )
    quantity = models.BigIntegerField(verbose_name="quantity")
    payment = models.ManyToManyField(Payment, related_name="gate_payment")
    status = models.SmallIntegerField(
        choices=GATESTATUS.choices, default=GATESTATUS.UNPAID
    )

    class Meta:
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
