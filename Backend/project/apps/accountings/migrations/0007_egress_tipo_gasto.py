# Generated by Django 5.0.4 on 2025-02-08 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountings', '0006_egress_acreedor_egress_seguro'),
    ]

    operations = [
        migrations.AddField(
            model_name='egress',
            name='tipo_gasto',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Tipo de Gasto'),
        ),
    ]
