# Generated by Django 5.0.4 on 2025-01-20 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='estados_fechas',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]