# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-16 08:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leadsMasterApp', '0012_auto_20161207_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='leadfrom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leadsMasterApp.Person'),
        ),
    ]
