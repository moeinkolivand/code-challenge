from django.contrib.auth import get_user_model
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
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
        This method makes a request to the external web service.
         We can check here whether the external service is available or not
        """
        return True

    def post(self, request, *args, **kwargs):
        user = User.objects.first()
        currency = Currency.objects.first()
        quantity = choice(list(range(1, 4)))
        payment = Payment.objects.create(
            user=user, currency=currency, quantity=quantity
        )
        wallet = Wallet.objects.get_or_create(user=user, balance=14)
        if payment.calculate_payment_price() >= 10:
            trsa = Transaction.objects.create(currency=currency, quantity=quantity)
            trsa.payment.add(payment)
            if trsa.buy_from_exchange(currency, quantity):
                with transaction.atomic():
                    try:
                        trsa.status = TRANSACTIONSTATUS.PAID.value
                        trsa.save(update_fields=["status"])
                        wallet.balance = (
                            F("balance") - payment.calculate_payment_price()
                        )
                        wallet.save(update_fields=["balance"])
                        WalletCurrency.objects.create(
                            currency, wallet, quantity, currency.price, user
                        )
                        payment.status = PAYMENTSTATUS.TRANSFERRED.value
                        payment.save(update_fields=["status"])
                        return Response(data={"paid": 1}, status=status.HTTP_201_CREATED)
                    except DatabaseError:
                        # According To Project That Be Custom !
                        raise APIException("There was a problem!")
        with transaction.atomic():
            transaction_list = (
                Transaction.objects.select_for_update()
                .select_related("currency", "user")
                .filter(currency=currency, status=TRANSACTIONSTATUS.UNPAID)
                .annotate(
                    price=ExpressionWrapper(
                        F("quantity") * F("currency__price"),
                        output_field=DecimalField(),
                    )
                )
            )
            all_price = transaction_list.aggregate(prc=Sum("price"))
            if self.buy_from_exchange(currency, all_price["prc"]):
                try:
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
                except DatabaseError:
                    # According To Project That Be Custom !
                    raise APIException("There was a problem!")

        return Response(data={"paid": 1}, status=status.HTTP_201_CREATED)
