# Generated by Django 4.2.5 on 2023-09-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinformation",
            name="national_card",
            field=models.ImageField(blank=True, upload_to="nationalcard"),
        ),
        migrations.AlterField(
            model_name="userinformation",
            name="recognizance",
            field=models.ImageField(blank=True, upload_to="recognizance"),
        ),
    ]