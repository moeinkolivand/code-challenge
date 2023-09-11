from django.contrib.auth import get_user_model
from django.db import models
from tethercodereview.models import BaseModel
from currency.models import Currency

User = get_user_model()


class Wallet(BaseModel):
    # User Wallet
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="User Wallet"
    )
    balance = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "wallet"
        verbose_name_plural = "wallets"


class WalletCurrency(BaseModel):
    """
    User Wallet Currencyies
    """

    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, verbose_name="currency", null=True
    )
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name="Wallet")
    quantity = models.BigIntegerField(verbose_name="quantity")
    buy_price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")

    def wallet_worth(self):
        """
        Calculate Current Currency Worth
        """
        return self.quantity * (self.currency.price - self.buy_price)

    class Meta:
        verbose_name = "walletcurrency"
        verbose_name_plural = "walletcurrencyies"
