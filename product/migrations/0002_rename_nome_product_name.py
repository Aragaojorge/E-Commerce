# Generated by Django 5.0.1 on 2024-02-07 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="nome",
            new_name="name",
        ),
    ]
