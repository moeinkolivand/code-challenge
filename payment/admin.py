from django.contrib import admin
from payment.models import Payment, Transaction


admin.site.register(Payment)
admin.site.register(Transaction)
