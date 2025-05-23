# Generated by Django 5.0.4 on 2025-01-09 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('InvestmentPlan', '0001_initial'),
        ('addresses', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='documents/', verbose_name='Imagen')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
            ],
            options={
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imágenes',
            },
        ),
        migrations.CreateModel(
            name='ImagenAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addresses.address')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pictures.imagen')),
            ],
            options={
                'verbose_name': 'Imagen de Dirección',
                'verbose_name_plural': 'Imágenes de Direcciones',
            },
        ),
        migrations.CreateModel(
            name='ImagenCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pictures.imagen')),
            ],
            options={
                'verbose_name': 'Imagen del Cliente',
                'verbose_name_plural': 'Imágenes de Clientes',
            },
        ),
        migrations.CreateModel(
            name='ImagenGuarantee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pictures.imagen')),
                ('investment_plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InvestmentPlan.investmentplan')),
            ],
            options={
                'verbose_name': 'Imagen de Garantía',
                'verbose_name_plural': 'Imágenes de Garantías',
            },
        ),
        migrations.CreateModel(
            name='ImagenOther',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=150, null=True, verbose_name='Descripción')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pictures.imagen')),
            ],
            options={
                'verbose_name': 'Otra Imagen',
                'verbose_name_plural': 'Otras Imágenes',
            },
        ),
    ]
