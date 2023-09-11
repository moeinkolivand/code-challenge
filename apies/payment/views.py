from django.contrib.auth import get_user_model
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from django.db.models.functions import Coalesce, Cast
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from random import choice
from currency.models import Currency
from payment.models import Payment, Transaction
from payment.enums import PAYMENTSTATUS, TRANSACTIONSTATUS
from wallet.models import Wallet, WalletCurrency
from django.db import DatabaseError, transaction


User = get_user_model()


class PaymentApiView(APIView):
    def buy_from_exchange(self, currency, quantity):
        """
        We Can Change  This Method To Be A Serializer Method Or Be A Class Method
        """
        return True

    def post(self, request, *args, **kwargs):
        user = User.objects.first()
        currency = Currency.objects.first()
        quantity = 2  # choice(list(range(1, 4)))
        payment = Payment.objects.create(
            user=user, currency=currency, quantity=quantity
        )
        wallet, _ = Wallet.objects.get_or_create(user=user)
        wallet.balance = F("balance") - payment.calculate_payment_price()
        wallet.save(update_fields=["balance"])
        if payment.calculate_payment_price() >= 10:
            trsa = Transaction.objects.create(
                currency=currency, quantity=quantity, payment=payment, user=user
            )
            if self.buy_from_exchange(currency, quantity):
                with transaction.atomic():
                    trsa.status = TRANSACTIONSTATUS.PAID.value
                    trsa.save(update_fields=["status"])
                    WalletCurrency.objects.create(
                        currency=currency,
                        wallet=wallet,
                        quantity=quantity,
                        buy_price=currency.price,
                        user=user,
                    )
                    payment.status = PAYMENTSTATUS.TRANSFERRED.value
                    payment.save(update_fields=["status"])
                    return Response(data={"paid": 1}, status=status.HTTP_201_CREATED)
        with transaction.atomic():
            transaction_list = (
                Transaction.objects.select_for_update()
                .select_related("currency", "user")
                .filter(currency=currency, status=TRANSACTIONSTATUS.UNPAID)
            )
            all_price = transaction_list.aggregate(
                prc=Coalesce(
                    Sum(F("quantity") * F("currency__price")),
                    0,
                    output_field=DecimalField(),
                )
            )
            if all_price["prc"] >= 10:
                if self.buy_from_exchange(currency, all_price["prc"]):
                    for tr in transaction_list:
                        tr.status = TRANSACTIONSTATUS.PAID.value
                    Transaction.objects.bulk_update(transaction_list, ("status",))
                    users_list = transaction_list.values_list("user", flat=True)
                    # TODO:: This Query Must Be Optimized
                    wallets = Wallet.objects.filter(user_id__in=users_list)
                    for wallet in wallets:
                        wallet.balance = (
                            F("balance") - payment.calculate_payment_price()
                        )
                    Wallet.objects.bulk_update(wallets, ("balance",))
                    WalletCurrency.objects.bulk_create(
                        [
                            WalletCurrency(
                                currency, wallet, quantity, currency.price, wallet.user
                            )
                            for wallet in wallets
                        ]
                    )
                    locked_payments = transaction_list.values_list(
                        "payment_id", flat=True
                    )
                    # TODO:: This Query Must Be Optimized
                    payments = Payment.objects.filter(id__in=locked_payments)
                    for payment in payments:
                        payment.status = PAYMENTSTATUS.TRANSFERRED.value
                    Payment.objects.bulk_update(payments, ("status",))
                    return Response(data={"paid": 1}, status=status.HTTP_201_CREATED)
        return Response(data={"paid": 0}, status=status.HTTP_201_CREATED)
