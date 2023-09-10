from django.contrib.auth import get_user_model
from django.db import models
from tethercodereview.models import BaseModel


User = get_user_model()


class Currency(BaseModel):
    name = models.CharField(max_length=126, verbose_name="Name")
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "currency"
        verbose_name_plural = 'currencies'
