from django.contrib.auth import get_user_model
from django.db import models
from payment.enums import PAYMENTSTATUS, TRANSACTIONSTATUS
from currency.models import Currency
from tethercodereview.models import BaseModel


User = get_user_model()


class Payment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, verbose_name="Currency"
    )
    # TODO:: We Can Change It TO Float Or Deciaml
    quantity = models.BigIntegerField(verbose_name="quantity")
    status = models.SmallIntegerField(
        choices=PAYMENTSTATUS.choices, default=PAYMENTSTATUS.NOT_TRANSFERRED
    )
    # We Can Add Field Price

    def calculate_payment_price(self):
        return self.currency.price * self.quantity

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class Transaction(BaseModel):
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, verbose_name="Currency"
    )
    # TODO:: We Can Change It TO Float Or Deciaml
    quantity = models.BigIntegerField(verbose_name="quantity")
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="gate_payment"
    )
    status = models.SmallIntegerField(
        choices=TRANSACTIONSTATUS.choices, default=TRANSACTIONSTATUS.UNPAID
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")

    class Meta:
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
