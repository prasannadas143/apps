# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-16 15:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0005_parentchilduser'),
    ]

    operations = [
        migrations.AddField(
            model_name='parentchilduser',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
