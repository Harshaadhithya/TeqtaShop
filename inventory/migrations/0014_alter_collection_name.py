# Generated by Django 4.1.1 on 2022-10-07 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0013_collection_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="name",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]