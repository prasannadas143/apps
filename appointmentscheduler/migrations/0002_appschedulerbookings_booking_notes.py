# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-23 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointmentscheduler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appschedulerbookings',
            name='booking_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
