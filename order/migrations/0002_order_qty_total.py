# Generated by Django 5.0.1 on 2024-02-19 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="qty_total",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
