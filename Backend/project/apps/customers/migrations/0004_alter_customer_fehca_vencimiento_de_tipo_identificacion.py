# Generated by Django 5.0.4 on 2024-10-29 15:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_customer_asesor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='fehca_vencimiento_de_tipo_identificacion',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Fecha de Vencimiento del Tipo de Identificacion'),
        ),
    ]