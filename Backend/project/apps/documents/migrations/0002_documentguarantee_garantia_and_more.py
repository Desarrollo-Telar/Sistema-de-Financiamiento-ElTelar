# Generated by Django 5.0.4 on 2024-11-09 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvestmentPlan', '0002_initial'),
        ('documents', '0001_initial'),
        ('financings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentguarantee',
            name='garantia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guarantee_documents', to='financings.detailsguarantees'),
        ),
        migrations.AlterField(
            model_name='documentguarantee',
            name='investment_plan_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='InvestmentPlan.investmentplan'),
        ),
    ]