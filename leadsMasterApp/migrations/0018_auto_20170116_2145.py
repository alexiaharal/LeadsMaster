# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadsMasterApp', '0017_auto_20170112_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalcontract',
            name='nextpayment',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lifecontract',
            name='nextpayment',
            field=models.DateField(blank=True, null=True),
        ),
    ]
