# Generated by Django 5.0.1 on 2024-01-22 08:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app1", "0020_requeste_receiver_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requeste",
            name="date_approved",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 22, 10, 12, 39, 491497)
            ),
        ),
        migrations.AlterField(
            model_name="requeste",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 22, 10, 12, 39, 491457)
            ),
        ),
        migrations.AlterField(
            model_name="requeste",
            name="state_progress",
            field=models.IntegerField(choices=[(1, "Pending"), (2, "Done")], default=1),
        ),
    ]