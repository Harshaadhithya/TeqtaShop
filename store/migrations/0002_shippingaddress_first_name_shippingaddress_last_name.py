# Generated by Django 4.1.1 on 2022-12-11 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shippingaddress",
            name="first_name",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="shippingaddress",
            name="last_name",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
