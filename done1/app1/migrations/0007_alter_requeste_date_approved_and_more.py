# Generated by Django 5.0.1 on 2024-01-18 12:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app1", "0006_alter_requeste_date_approved_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requeste",
            name="date_approved",
            field=models.DateTimeField(
                verbose_name=datetime.datetime(
                    2024, 1, 18, 12, 17, 27, 536857, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="requeste",
            name="date_created",
            field=models.DateTimeField(
                verbose_name=datetime.datetime(2024, 1, 18, 12, 17, 27, 536800)
            ),
        ),
    ]