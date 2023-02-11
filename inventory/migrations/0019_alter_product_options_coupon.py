# Generated by Django 4.1.1 on 2023-02-07 16:35

from django.db import migrations, models
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0018_compatibilty_productvariant_compatible_with"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product", options={"ordering": ["-created"]},
        ),
        migrations.CreateModel(
            name="Coupon",
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
                ("name", models.CharField(max_length=200, unique=True)),
                (
                    "coupon_type",
                    models.CharField(
                        choices=[
                            ("percentage", "percentage"),
                            ("cashback", "cashback"),
                        ],
                        max_length=200,
                    ),
                ),
                ("value", models.PositiveBigIntegerField()),
                ("min_checkout_price", models.PositiveBigIntegerField(default=1)),
                ("is_active", models.BooleanField(default=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "applicable_products",
                    models.ManyToManyField(
                        blank=True,
                        default=inventory.models.productsList,
                        to="inventory.product",
                    ),
                ),
            ],
        ),
    ]