# Generated by Django 5.0.1 on 2024-01-18 12:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app1", "0011_alter_requeste_date_approved_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requeste",
            name="date_approved",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 18, 14, 45, 49, 162439)
            ),
        ),
        migrations.AlterField(
            model_name="requeste",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 18, 14, 45, 49, 162401)
            ),
        ),
    ]
