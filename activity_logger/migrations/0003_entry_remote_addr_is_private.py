# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_logger', '0002_auto_20160420_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='remote_addr_is_private',
            field=models.NullBooleanField(),
        ),
    ]
