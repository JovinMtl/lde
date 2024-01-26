# Generated by Django 5.0.1 on 2024-01-24 09:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portefeuille", "0006_alter_lumiclientrequeste_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lumiclientrequeste",
            name="date_approved",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 24, 9, 29, 49, 396230)
            ),
        ),
        migrations.AlterField(
            model_name="lumiclientrequeste",
            name="date_requested",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 24, 9, 29, 49, 396185)
            ),
        ),
    ]
