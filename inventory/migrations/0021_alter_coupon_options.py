# Generated by Django 4.1.1 on 2023-02-08 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0020_remove_coupon_is_active_coupon_status_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="coupon", options={"ordering": ["status", "-created"]},
        ),
    ]