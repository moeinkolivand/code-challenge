# Generated by Django 4.2.5 on 2023-09-10 14:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_alter_userinformation_national_card_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="baseuser",
            name="phone_number",
            field=models.CharField(
                max_length=11, unique=True, verbose_name="Phone Number"
            ),
        ),
    ]
