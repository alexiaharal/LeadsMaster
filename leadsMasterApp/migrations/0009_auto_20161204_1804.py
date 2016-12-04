# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-04 18:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadsMasterApp', '0008_auto_20161204_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='password',
            field=models.CharField(default='password2', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='wasclient',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], default=0),
        ),
        migrations.AlterField(
            model_name='generalcontract',
            name='annualpremium',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lifecontract',
            name='annualpremium',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]