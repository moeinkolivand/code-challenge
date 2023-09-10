from django.contrib import admin

from wallet.models import Wallet,WalletCurrency

admin.site.register(Wallet)
admin.site.register(WalletCurrency)
