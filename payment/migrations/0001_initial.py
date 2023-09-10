# Generated by Django 4.2.5 on 2023-09-10 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("currency", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                ("quantity", models.BigIntegerField(verbose_name="quantity")),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(0, "NOT TRANSFERRED"), (1, "TRANSFERRED")], default=0
                    ),
                ),
                (
                    "currency",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="currency.currency",
                        verbose_name="Currency",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment",
                "verbose_name_plural": "Payments",
            },
        ),
        migrations.CreateModel(
            name="TRANSACTION",
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
                ("quantity", models.BigIntegerField(verbose_name="quantity")),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(0, "Un Paid"), (1, "Paid")], default=0
                    ),
                ),
                (
                    "currency",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="currency.currency",
                        verbose_name="Currency",
                    ),
                ),
                (
                    "payment",
                    models.ManyToManyField(
                        related_name="gate_payment", to="payment.payment"
                    ),
                ),
            ],
            options={
                "verbose_name": "transaction",
                "verbose_name_plural": "transactions",
            },
        ),
    ]