from __future__ import unicode_literals
from django import forms
from django.db import models

# Create your models here.



class Company(models.Model):
    idcompany = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)  # Field name made lowercase.

class Person(models.Model):
    client_CHOICES = (
        (1, 'Yes'),
        (0, 'No'),
    )
    introducer_CHOICES = (
        (1, 'Yes'),
        (0, 'No'),
    )
    idperson = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    telephone = models.CharField( max_length = 15)
    email = models.CharField( max_length=45, blank=True, null=True)
    dateofbirth = models.DateField()  # Field name made lowercase.
    isintroducer = models.IntegerField(choices=introducer_CHOICES, default=0)  # Field name made lowercase.
    isclient = models.IntegerField(choices=client_CHOICES,default=0)  # Field name made lowercase.
    leadfrom = models.IntegerField()  # Field name made lowercase.


class Generalbusinessplans(models.Model):
    planid = models.AutoField(primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45)  # Field name made lowercase.
    company = models.ForeignKey(Company)  # Field name made lowercase.
    commission = models.FloatField()  # Field name made lowercase.

class Lifebusinessplans(models.Model):
    planlifeid = models.AutoField( primary_key=True)  # Field name made lowercase.
    name = models.CharField( max_length=45)  # Field name made lowercase.
    company = models.ForeignKey(Company)  # Field name made lowercase.
    firstyearcommission = models.FloatField()  # Field name made lowercase.
    maxpercentage = models.IntegerField( blank=True, null=True)  # Field name made lowercase.
    minpercentage = models.IntegerField( blank=True, null=True)  # Field name made lowercase.
    futureprofit = models.FloatField()  # Field name made lowercase.
    futureprofit2 = models.FloatField(blank=True, null=True)  # Field name made lowercase.
    futureprofit3 = models.FloatField(blank=True, null=True)  # Field name made lowercase.
    futureprofit4 = models.FloatField( blank=True, null=True)  # Field name made lowercase.
    agelimit = models.IntegerField()  # Field name made lowercase.
    duration = models.IntegerField()  # Field name made lowercase.

class LifeContract(models.Model):
    idcontract = models.IntegerField(primary_key=True)
    client= models.ForeignKey(Person)
    issuedate = models.DateTimeField('date issued')
    expirationdate = models.DateTimeField('expiration date')
    plan = models.ManyToManyField(Lifebusinessplans)
    annualpremium = models.FloatField(blank=True, null=True)
    doses = models.IntegerField(blank=True, null=True)
    nextpayment = models.DateTimeField(blank=True, null=True)
    price = models.FloatField()
    notes = models.CharField(max_length =80)

class GeneralContract(models.Model):
    idcontract = models.IntegerField(primary_key=True)
    client=models.ForeignKey(Person)
    issuedate = models.DateTimeField()  # Field name made lowercase.
    expirationdate = models.DateTimeField()  # Field name made lowercase.
    plan = models.ManyToManyField(Generalbusinessplans)
    annualpremium = models.FloatField( blank=True, null=True)  # Field name made lowercase.
    doses = models.IntegerField(blank=True, null=True)
    nextpayment = models.DateTimeField( blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField()
    notes = models.CharField(max_length =80)


class Employee(models.Model):
    employeeid = models.OneToOneField(Person, primary_key=True)  # Field name made lowercase.
    position = models.CharField( max_length=45)  # Field name made lowercase.
    salary = models.FloatField()  # Field name made lowercase.
    hourspermonth = models.IntegerField()  # Field name made lowercase.

class Activity(models.Model):
    activityid = models.AutoField(primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Person, blank=True, null=True)  # Field name made lowercase.
    duration = models.IntegerField()  # Field name made lowercase.
    datetime = models.DateTimeField()  # Field name made lowercase.
    activityname = models.CharField(max_length=45)  # Field name made lowercase.

class Calendar(models.Model):
    entryid = models.AutoField(primary_key=True)  # Field name made lowercase.
    activity = models.ForeignKey(Activity)
    employee = models.ForeignKey(Employee)