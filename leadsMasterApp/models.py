from __future__ import unicode_literals

from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Person Model
class Person(models.Model):
    client_CHOICES = (
        (1, 'Yes'),
        (0, 'No'),
    )
    introducer_CHOICES = (
        (1, 'Yes'),
        (0, 'No'),
    )
    gender_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    occupation_CHOICES = (
        ("Student", "Student"),
        ("Banker", "Banker"),
        ("Education Staff ", "Education Staff"),
        ("Lawyer", "Lawyer"),
        ("Enterpreneur", "Enterpreneur"),
        ("Customer Service Employee", "Customer Service Employee"),
        ("Public Sector ", "Public Sector"),
        ("Private Sector ", "Private Sector"),
        ("Other", "Other")
    )
    id = models.AutoField(primary_key=True, unique=True)
    idperson = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    gender = models.CharField(choices=gender_CHOICES, default="Male", max_length=6)
    telephone = models.CharField(max_length=15)
    email = models.CharField(max_length=45, blank=True, null=True)
    dateofbirth = models.DateField()  # Field name made lowercase.
    occupation = models.CharField(choices=occupation_CHOICES, default="None", max_length=60)
    isintroducer = models.IntegerField(choices=introducer_CHOICES, default=0)  # Field name made lowercase.
    isclient = models.IntegerField(choices=client_CHOICES, default=0)  # Field name made lowercase.
    leadfrom = models.ForeignKey('self', blank=True, null=True)  # Field name made lowercase.
    wasclient = models.IntegerField(choices=client_CHOICES, default=0)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return str(self.name) + ' ' + str(self.surname) + ' -- ' + str(self.idperson)


# UserProfile Model
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    employeeid = models.OneToOneField(Person, primary_key=True)  # Field name made lowercase.
    position = models.CharField(max_length=45)  # Field name made lowercase.
    salary = models.FloatField()  # Field name made lowercase.
    hourspermonth = models.IntegerField()  # Field name made lowercase.

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


# Company Model
class Company(models.Model):
    idcompany = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)  # Field name made lowercase.

    def __unicode__(self):
        return str(self.name)


# General Business Plans Model
class Generalbusinessplans(models.Model):
    planid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    company = models.ForeignKey(Company)
    commission = models.FloatField()
    deleted = models.BooleanField(default=False);

    def __unicode__(self):
        return str(self.company) + ' -- ' + str(self.name)


# Life Business Plans Model
class Lifebusinessplans(models.Model):
    planlifeid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    company = models.ForeignKey(Company)
    firstyearcommission = models.FloatField()
    maxpercentage = models.IntegerField(blank=True, null=True)
    minpercentage = models.IntegerField(blank=True, null=True)
    futureprofit = models.FloatField()
    futureprofit2 = models.FloatField(blank=True, null=True)
    futureprofit3 = models.FloatField(blank=True, null=True)
    futureprofit4 = models.FloatField(blank=True, null=True)
    agelimit = models.IntegerField()
    deleted = models.BooleanField(default=False);

    def __unicode__(self):
        return str(self.company) + ' -- ' + str(self.name)


# Life Contract Model
class LifeContract(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    idcontract = models.IntegerField()
    client = models.ForeignKey(Person)
    issuedate = models.DateField('date issued')
    expirationdate = models.DateField('expiration date')
    plan = models.ManyToManyField(Lifebusinessplans)
    basicvalue = models.FloatField()
    doses = models.IntegerField()
    nextpayment = models.DateField(blank=True, null=True)
    annualpremium = models.FloatField()
    duration = models.IntegerField(blank=True, null=True)
    notes = models.CharField(max_length=80)
    cancelled = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.idcontract) + ' -- ' + '\n'.join(p.name for p in self.plan.all())


# General Contract Model
class GeneralContract(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    idcontract = models.IntegerField()
    client = models.ForeignKey(Person)
    issuedate = models.DateField()
    expirationdate = models.DateField()
    plan = models.ManyToManyField(Generalbusinessplans)
    basicvalue = models.FloatField()
    doses = models.IntegerField()
    nextpayment = models.DateField(blank=True, null=True)
    years = models.IntegerField(default=1)
    annualpremium = models.FloatField()
    notes = models.CharField(max_length=80)
    cancelled = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.idcontract) + ' -- ' + '\n'.join(p.name for p in self.plan.all())


# Employee Model
class Employee(models.Model):
    employeeid = models.OneToOneField(Person, primary_key=True)  # Field name made lowercase.
    position = models.CharField(max_length=45)  # Field name made lowercase.
    salary = models.FloatField()  # Field name made lowercase.
    hourspermonth = models.IntegerField()  # Field name made lowercase.
    password = models.CharField(max_length=40)


# Activity Model
class Activity(models.Model):
    activityid = models.AutoField(primary_key=True)  # Field name made lowercase.
    activityname = models.CharField(max_length=45)  # Field name made lowercase.
    customerid = models.ForeignKey(Person, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(default=timezone.now)  # Field name made lowercase.
    time = models.TimeField(default=timezone.now)
    duration = models.IntegerField()  # Field name made lowercase.
    meeting_minutes = models.CharField(max_length=200, blank=True, null=True)
    email = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.activityname + ' -- ' + str(self.date))


# Calendar Model
class Calendar(models.Model):
    entryid = models.AutoField(primary_key=True)  # Field name made lowercase.
    activity = models.ForeignKey(Activity)
    employee = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return str(self.entryid)


##### Notification Component Models ######

class birthdayNot(models.Model):
    id = models.AutoField(primary_key=True)
    birthday = models.ForeignKey(Person)
    date = models.DateField(default=timezone.now)
    email = models.BooleanField()


class genRenewalsNot(models.Model):
    id = models.AutoField(primary_key=True)
    renewal = models.ForeignKey(GeneralContract)
    date = models.DateField(default=timezone.now)
    email = models.BooleanField()


class lifeRenewalsNot(models.Model):
    id = models.AutoField(primary_key=True)
    renewal = models.ForeignKey(LifeContract)
    date = models.DateField(default=timezone.now)
    email = models.BooleanField()


class genPaymentsNot(models.Model):
    id = models.AutoField(primary_key=True)
    payment = models.ForeignKey(GeneralContract)
    date = models.DateField(default=timezone.now)
    email = models.BooleanField()


class lifePaymentsNot(models.Model):
    id = models.AutoField(primary_key=True)
    payment = models.ForeignKey(LifeContract)
    date = models.DateField(default=timezone.now)
    email = models.BooleanField()
