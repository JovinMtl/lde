# Generated by Django 5.0.1 on 2024-02-02 08:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app1", "0006_alter_differente_date_alter_recharge_date_action_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="trade",
            name="date",
            field=models.DateField(
                default=datetime.datetime(2024, 2, 2, 10, 43, 9, 128463)
            ),
        ),
        migrations.AlterField(
            model_name="differente",
            name="date",
            field=models.DateField(
                default=datetime.datetime(2024, 2, 2, 10, 43, 9, 128203)
            ),
        ),
        migrations.AlterField(
            model_name="recharge",
            name="date_action",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 2, 10, 43, 9, 127944)
            ),
        ),
        migrations.AlterField(
            model_name="requeste",
            name="date_approved",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 2, 10, 43, 9, 127559)
            ),
        ),
        migrations.AlterField(
            model_name="requeste",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 2, 2, 10, 43, 9, 127545)
            ),
        ),
    ]
