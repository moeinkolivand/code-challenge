from django.urls import path, include
from apies.user.views import HelloApi

urlpatterns = [
    path("hello", HelloApi.as_view(), name="hello world"),
    path("payment/", include("apies.payment.urls")),
]
