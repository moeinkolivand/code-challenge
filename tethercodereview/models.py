from django.db import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created_time")
    modified_time = models.DateTimeField(auto_now=True, verbose_name="modified_time")

    class Meta:
        abstract = True
