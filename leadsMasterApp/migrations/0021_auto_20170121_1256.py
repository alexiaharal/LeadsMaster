# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-21 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadsMasterApp', '0020_auto_20170119_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalcontract',
            name='doses',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lifecontract',
            name='doses',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]