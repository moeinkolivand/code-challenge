from django.urls import path
from apies.payment.views import PaymentApiView

urlpatterns = [path("buy", PaymentApiView.as_view(), name="buy_currency")]
