# Generated by Django 5.0.4 on 2024-05-20 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_product_or_service', models.CharField(max_length=75)),
                ('total_value_of_the_product_or_service', models.CharField(max_length=75)),
                ('investment_plan_description', models.TextField(blank=True, null=True)),
                ('initial_amount', models.CharField(max_length=75)),
                ('monthly_amount', models.CharField(max_length=75)),
                ('transfers_or_transfer_of_funds', models.BooleanField()),
                ('type_of_transfers_or_transfer_of_funds', models.CharField(choices=[('Local', 'Local'), ('Internacional', 'Internacional')], max_length=75)),
            ],
        ),
    ]