# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-29 13:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadsMasterApp', '0003_auto_20161229_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lifecontract',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
