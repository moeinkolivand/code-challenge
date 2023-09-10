from django.contrib import admin
from payment.models import Payment, TRANSACTION


admin.site.register(Payment)
admin.site.register(TRANSACTION)
