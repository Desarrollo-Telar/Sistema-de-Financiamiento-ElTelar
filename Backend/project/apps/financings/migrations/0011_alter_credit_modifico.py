# Generated by Django 5.0.4 on 2025-04-23 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financings', '0010_alter_credit_numero_credito_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='modifico',
            field=models.BooleanField(default=False, verbose_name='MOdificacion'),
        ),
    ]
