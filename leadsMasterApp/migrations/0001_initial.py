# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-15 10:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('activityid', models.AutoField(primary_key=True, serialize=False)),
                ('duration', models.IntegerField()),
                ('datetime', models.DateTimeField()),
                ('activityname', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('entryid', models.AutoField(primary_key=True, serialize=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leadsMasterApp.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('idcompany', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Generalbusinessplans',
            fields=[
                ('planid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('commission', models.FloatField(db_column='Commission')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leadsMasterApp.Company')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralContract',
            fields=[
                ('idcontract', models.IntegerField(primary_key=True, serialize=False)),
                ('issuedate', models.DateTimeField()),
                ('expirationdate', models.DateTimeField()),
                ('annualpremium', models.FloatField(blank=True, null=True)),
                ('doses', models.IntegerField(blank=True, null=True)),
                ('nextpayment', models.DateTimeField(blank=True, null=True)),
                ('notes', models.CharField(max_length=80)),
                ('plan', models.ManyToManyField(to='leadsMasterApp.Generalbusinessplans')),
            ],
        ),
        migrations.CreateModel(
            name='Lifebusinessplans',
            fields=[
                ('planlifeid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('firstyearcommission', models.FloatField()),
                ('maxpercentage', models.IntegerField(blank=True, null=True)),
                ('minpercentage', models.IntegerField(blank=True, null=True)),
                ('futureprofit1', models.FloatField()),
                ('futureprofit2', models.FloatField(blank=True, null=True)),
                ('futureprofit3', models.FloatField(blank=True, null=True)),
                ('futureprofit4', models.FloatField(blank=True, null=True)),
                ('agelimit', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leadsMasterApp.Company')),
            ],
        ),
        migrations.CreateModel(
            name='LifeContract',
            fields=[
                ('idcontract', models.IntegerField(primary_key=True, serialize=False)),
                ('issuedate', models.DateTimeField(verbose_name='date issued')),
                ('expirationdate', models.DateTimeField(verbose_name='expiration date')),
                ('annualpremium', models.FloatField(blank=True, null=True)),
                ('doses', models.IntegerField(blank=True, null=True)),
                ('nextpayment', models.DateTimeField(blank=True, null=True)),
                ('notes', models.CharField(max_length=80)),
                ('plan', models.ManyToManyField(to='leadsMasterApp.Lifebusinessplans')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('idperson', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('telephone', models.CharField(max_length=15)),
                ('email', models.CharField(blank=True, max_length=45, null=True)),
                ('dateofbirth', models.DateField()),
                ('isintroducer', models.IntegerField()),
                ('isclient', models.IntegerField()),
                ('leadfrom', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employeeid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='leadsMasterApp.Person')),
                ('position', models.CharField(max_length=45)),
                ('salary', models.FloatField()),
                ('hourspermonth', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='generalcontracts',
            field=models.ManyToManyField(blank=True, to='leadsMasterApp.GeneralContract'),
        ),
        migrations.AddField(
            model_name='person',
            name='lifecontracts',
            field=models.ManyToManyField(blank=True, to='leadsMasterApp.LifeContract'),
        ),
        migrations.AddField(
            model_name='activity',
            name='customerid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leadsMasterApp.Person'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leadsMasterApp.Employee'),
        ),
    ]
