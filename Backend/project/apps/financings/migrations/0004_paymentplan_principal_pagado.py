# Generated by Django 5.0.4 on 2024-11-27 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financings', '0003_cuota'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentplan',
            name='principal_pagado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Capital'),
        ),
    ]