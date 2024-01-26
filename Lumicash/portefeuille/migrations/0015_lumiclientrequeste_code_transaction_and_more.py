# Generated by Django 5.0.1 on 2024-01-25 16:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portefeuille", "0014_alter_lumiclientrequeste_date_approved_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="lumiclientrequeste",
            name="code_transaction",
            field=models.CharField(default="xx", max_length=15),
        ),
        migrations.AlterField(
            model_name="lumiclientrequeste",
            name="date_approved",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 25, 16, 33, 21, 89978)
            ),
        ),
        migrations.AlterField(
            model_name="lumiclientrequeste",
            name="date_requested",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 25, 16, 33, 21, 89940)
            ),
        ),
    ]
