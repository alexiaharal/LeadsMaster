# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-11 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadsMasterApp', '0014_generalcontract_years'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalcontract',
            name='years',
            field=models.IntegerField(default=0),
        ),
    ]
