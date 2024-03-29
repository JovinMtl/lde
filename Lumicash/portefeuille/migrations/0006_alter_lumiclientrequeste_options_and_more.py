# Generated by Django 5.0.1 on 2024-01-24 09:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portefeuille", "0005_lumiclientrequeste_link_activate_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="lumiclientrequeste",
            options={"verbose_name": "IGisabo", "verbose_name_plural": "IBisabo"},
        ),
        migrations.AddField(
            model_name="lumiclientrequeste",
            name="amount_to_pay",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="lumiclientrequeste",
            name="date_approved",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 24, 9, 25, 48, 378325)
            ),
        ),
        migrations.AlterField(
            model_name="lumiclientrequeste",
            name="date_requested",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 24, 9, 25, 48, 378290)
            ),
        ),
    ]
