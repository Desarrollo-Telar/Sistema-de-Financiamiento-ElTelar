# Generated by Django 5.0.4 on 2024-07-18 21:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('roles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='idUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rol_usuario', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]