from django.urls import path
from apies.user.views import HelloApi


urlpatterns = [
    path("hello", HelloApi.as_view(), name="hello world"),
]
