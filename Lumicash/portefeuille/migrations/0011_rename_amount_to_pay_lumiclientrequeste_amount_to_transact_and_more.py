# Generated by Django 5.0.1 on 2024-01-24 10:17

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "portefeuille",
            "0010_rename_creditor_phone_number_lumiclientrequeste_benefitor_phone_number_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="lumiclientrequeste",
            old_name="amount_to_pay",
            new_name="amount_to_transact",
        ),
        migrations.RemoveField(
            model_name="lumiclientrequeste",
            name="benefitor_phone_number",
        ),
        migrations.RemoveField(
            model_name="lumiclientrequeste",
            name="owner_username",
        ),
        migrations.RemoveField(
            model_name="lumiclientrequeste",
            name="request_benefitor",
        ),
        migrations.AddField(
            model_name="lumiclientrequeste",
            name="benefitor",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="benefiting_lumi_client_requestes",
                to="portefeuille.portefeuilleclient",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="lumiclientrequeste",
            name="date_approved",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 24, 10, 16, 47, 154754)
            ),
        ),
        migrations.AlterField(
            model_name="lumiclientrequeste",
            name="date_requested",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 24, 10, 16, 47, 154733)
            ),
        ),
        migrations.AlterField(
            model_name="lumiclientrequeste",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owned_lumi_client_requestes",
                to="portefeuille.portefeuilleclient",
            ),
        ),
    ]