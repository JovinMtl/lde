# Generated by Django 5.0.1 on 2024-02-01 20:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app1", "0002_delete_lid_remove_recharge_anything_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="portefeuille",
            name="uid",
        ),
        migrations.AlterField(
            model_name="differente",
            name="date",
            field=models.DateField(
                default=datetime.datetime(2024, 2, 1, 22, 48, 47, 35932)
            ),
        ),
        migrations.AlterField(
            model_name="recharge",
            name="date_action",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 1, 22, 48, 47, 35234)
            ),
        ),
        migrations.AlterField(
            model_name="requeste",
            name="date_approved",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 1, 22, 48, 47, 34109)
            ),
        ),
        migrations.AlterField(
            model_name="requeste",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 1, 22, 48, 47, 34071)
            ),
        ),
    ]