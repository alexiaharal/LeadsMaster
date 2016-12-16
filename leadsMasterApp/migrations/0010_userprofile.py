# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 12:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leadsMasterApp', '0009_auto_20161204_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('website', models.URLField(blank=True)),
                ('employeeid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='leadsMasterApp.Person')),
                ('position', models.CharField(max_length=45)),
                ('salary', models.FloatField()),
                ('hourspermonth', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
