# Generated by Django 5.0.4 on 2024-05-20 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('FinancialInformation', '0001_initial'),
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='othersourcesofincome',
            name='address_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addresses.address'),
        ),
    ]