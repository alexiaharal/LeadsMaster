# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-08 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadsMasterApp', '0012_auto_20170107_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalcontract',
            name='expirationdate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='generalcontract',
            name='issuedate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='lifecontract',
            name='expirationdate',
            field=models.DateField(verbose_name='expiration date'),
        ),
        migrations.AlterField(
            model_name='lifecontract',
            name='issuedate',
            field=models.DateField(verbose_name='date issued'),
        ),
    ]
