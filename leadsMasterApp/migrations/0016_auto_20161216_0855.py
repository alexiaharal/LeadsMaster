# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-16 08:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leadsMasterApp', '0015_auto_20161216_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='leadfrom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leadsMasterApp.Person'),
        ),
    ]
