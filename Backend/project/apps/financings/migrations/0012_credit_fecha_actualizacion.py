# Generated by Django 5.0.4 on 2025-05-26 22:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financings', '0011_alter_credit_modifico'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='fecha_actualizacion',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Fecha en que se actualizo el credito'),
        ),
    ]
