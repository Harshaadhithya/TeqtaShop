# Generated by Django 4.1.1 on 2022-10-03 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0008_alter_productvariant_available_stock_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productvariant",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_variants",
                to="inventory.product",
            ),
        ),
    ]
