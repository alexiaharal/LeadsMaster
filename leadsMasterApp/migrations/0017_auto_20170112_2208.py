# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-12 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadsMasterApp', '0016_auto_20170112_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalcontract',
            name='years',
            field=models.IntegerField(default=1),
        ),
    ]
