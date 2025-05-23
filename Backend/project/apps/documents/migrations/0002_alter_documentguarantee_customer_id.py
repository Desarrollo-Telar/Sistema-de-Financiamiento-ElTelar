# Generated by Django 5.0.4 on 2025-02-08 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_alter_customer_email'),
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentguarantee',
            name='customer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guarantee_documents', to='customers.customer'),
        ),
    ]
