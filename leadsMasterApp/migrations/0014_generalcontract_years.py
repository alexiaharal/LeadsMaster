# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-09 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadsMasterApp', '0013_auto_20170108_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalcontract',
            name='years',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
