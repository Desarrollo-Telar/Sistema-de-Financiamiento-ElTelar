# Generated by Django 5.0.4 on 2025-07-01 16:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Titulo')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Mensaje')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='Para')),
            ],
            options={
                'verbose_name': 'Notificacion',
                'verbose_name_plural': 'Notificaciones',
                'ordering': ['-created_at'],
            },
        ),
    ]
