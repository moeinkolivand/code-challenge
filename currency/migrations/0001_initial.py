# Generated by Django 4.2.5 on 2023-09-10 14:25

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created_time"
                    ),
                ),
                (
                    "modified_time",
                    models.DateTimeField(auto_now=True, verbose_name="modified_time"),
                ),
                ("name", models.CharField(max_length=126, verbose_name="Name")),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                "verbose_name": "currency",
                "verbose_name_plural": "currencies",
            },
        ),
    ]
