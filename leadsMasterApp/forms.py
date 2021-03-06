from collections import OrderedDict

from django.db import models
from django.forms import ModelForm, extras
from django import forms
from leadsMasterApp.models import Person, UserProfile, Lifebusinessplans, Generalbusinessplans, LifeContract, \
    GeneralContract, Company, \
    Activity, Calendar
from django.contrib.auth.models import User
from django import forms
from datetime import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

# These are the years that are shown in every date selection. Can be amended with the passage of the years
DOY = ('1926', '1927', '1928', '1929', '1930', '1931', '1932', '1933', '1934', '1935', '1936', '1937',
       '1938', '1939', '1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949',
       '1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960',
       '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972',
       '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984',
       '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
       '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
       '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018',
       '2019', '2020', '2021', '2022', '2023', '2024', '2025')


# User Form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


# User Profile form with addition fields
# I.e. This is an employee entity
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('employeeid', 'position', 'salary', 'hourspermonth')
        labels = {
            "employeeid": "Employee ID",
            'position': 'Position',
            'salary': 'Salary',
            'hourspermonth': 'Working Hours Per Month'
        }


# Profile Form , i.e. Person Model
class PersonForm(forms.ModelForm):
    dateofbirth = forms.DateField(label='Date Of Birth  ', widget=extras.SelectDateWidget(years=DOY))

    class Meta:
        model = Person
        fields = ['idperson', 'name', 'surname', 'gender', 'telephone', 'email', 'dateofbirth', 'occupation',
                  'isclient', 'isintroducer', 'leadfrom', 'wasclient']
        labels = {
            "idperson": "Person ID",
            "name": "Name",
            'surname': 'Surname',
            'gender': 'Gender',
            'telephone': 'Telephone',
            'email': 'Email',
            'dateofbirth': 'Date Of Birth',
            'occupation': 'Occupation',
            'isclient': 'Is Client?',
            'isintroducer': 'Is Introducer?',
            'leadfrom': 'Lead From Person: ',
            'wasclient': 'Has Cancelled Contracts ?'
        }


# Life Contract From
class LifeContractForm(forms.ModelForm):
    # Get Life Plans from Lifebusinessplans model
    def __init__(self, *args, **kwargs):
        super(LifeContractForm, self).__init__(*args, **kwargs)
        self.fields['plan'].queryset = Lifebusinessplans.objects.filter(deleted=False)

    # Date widgets used for a more user friendly gui
    issuedate = forms.DateField(widget=extras.SelectDateWidget(years=DOY), initial=datetime.now(), label="Issue Date")
    expirationdate = forms.DateField(widget=extras.SelectDateWidget(years=DOY), initial=datetime.now(),
                                     label="Expiration Date")
    nextpayment = forms.DateField(widget=extras.SelectDateWidget(years=DOY), initial=datetime.now(),
                                  label="Next Payment Date")

    class Meta:
        model = LifeContract
        fields = ['idcontract', 'client', 'issuedate', 'expirationdate', 'plan',
                  'basicvalue', 'doses', 'nextpayment', 'annualpremium', 'duration', 'notes', 'cancelled']
        labels = {
            'idcontract': 'Contract ID',
            'client': 'Client',
            'issuedate': 'Issue Date',
            'expirationdate': 'Expiration Date',
            'plan': 'Plans Included',
            'basicvalue': 'Basic Value',
            'doses': 'Payment Doses',
            'nextpayment': 'Next Payment Due',
            'annualpremium': 'Annual Premium',
            'duration': 'Duration',
            'notes': 'Comments',
            'cancelled': 'Do you want to cancel this contract?'
        }


# General Contract Form
class GeneralContractForm(forms.ModelForm):
    # Get General Plans from Generalbusinessplans model
    def __init__(self, *args, **kwargs):
        super(GeneralContractForm, self).__init__(*args, **kwargs)
        self.fields['plan'].queryset = Generalbusinessplans.objects.filter(deleted=False)

    # Date widgets used for a more user friendly gui
    issuedate = forms.DateField(widget=extras.SelectDateWidget(years=DOY), initial=datetime.now(), label="Issue Date")
    expirationdate = forms.DateField(widget=extras.SelectDateWidget(years=DOY), initial=datetime.now(),
                                     label="Expiration Date")
    nextpayment = forms.DateField(widget=extras.SelectDateWidget(years=DOY), initial=datetime.now(),
                                  label="Next Payment Date")

    class Meta:
        model = GeneralContract
        fields = ['idcontract', 'client', 'issuedate', 'expirationdate', 'plan',
                  'basicvalue', 'doses', 'nextpayment', 'annualpremium', 'notes', 'cancelled']
        labels = {
            'idcontract': 'Contract ID',
            'client': 'Client',
            'issuedate': 'Issue Date',
            'expirationdate': 'Expiration Date',
            'plan': 'Plans Included',
            'basicvalue': 'Basic Value',
            'doses': 'Payment Doses',
            'nextpayment': 'Next Payment Due',
            'annualpremium': 'Annual Premium',
            'notes': 'Comments',
            'cancelled': 'Do you want to cancel this contract?'

        }


# Edit/Add Company Form, i.e. Company Model
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = {'idcompany', 'name'}
        labels = {
            'idcompany': 'Company ID',
            'name': 'Name'
        }


# Edit/Add General Plan, i.e. Generalbusinessplans model
class GeneralPlansForm(forms.ModelForm):
    ORDER = ('name', 'company', 'commission','deleted')

    def __init__(self, *args, **kwargs):
        super(GeneralPlansForm, self).__init__(*args, **kwargs)
        fields = OrderedDict()
        for key in self.ORDER:
            fields[key] = self.fields.pop(key)
        self.fields = fields

    class Meta:
        model = Generalbusinessplans
        fields = {'planid', 'name', 'company', 'commission','deleted'}
        labels = {
            'planid': 'Plan ID',
            'name': 'Name',
            'company': 'Company Related',
            'commission': 'Commission For This Plan',
            'deleted': 'Would you like to delete this plan?'
        }


# Edit/Add Life Plan, i.e. Lifebusinessplans model
class LifePlansForm(forms.ModelForm):
    ORDER = ('name', 'company', 'firstyearcommission',
             'futureprofit', 'futureprofit2', 'futureprofit3', 'futureprofit4',
             'maxpercentage', 'minpercentage', 'agelimit','deleted')

    def __init__(self, *args, **kwargs):
        super(LifePlansForm, self).__init__(*args, **kwargs)
        fields = OrderedDict()
        for key in self.ORDER:
            fields[key] = self.fields.pop(key)
        self.fields = fields

    class Meta:
        model = Lifebusinessplans
        fields = {'planlifeid', 'name', 'company', 'firstyearcommission',
                  'maxpercentage', 'minpercentage', 'futureprofit', 'futureprofit2',
                  'futureprofit3', 'futureprofit4', 'agelimit','deleted'}
        labels = {'planlifeid': 'Plan ID',
                  'name': 'Name',
                  'company': 'Company Related',
                  'firstyearcommission': 'First Year Commission',
                  'maxpercentage': 'Maximum Commission Percentage',
                  'minpercentage': 'Minimum Commission Percentage',
                  'futureprofit': 'Profit For Future/Second Year',
                  'futureprofit2': 'Profit For Third Year (If applicable)',
                  'futureprofit3': 'Profit For Fourth Year (If applicable)',
                  'futureprofit4': 'Profit For Fourth Year (If applicable)',
                  'agelimit': 'Age Limit of Plan',
                  'deleted': 'Would you like to delete this plan?'
                  }


# Search Form/Bar used in various places
class SearchForm(forms.Form):
    searchbox = forms.CharField(label='Search: ')


# Plans Selection Form, used in Reports section to select particular plan results
class PlansOptionsForm(forms.Form):
    lifePlan = forms.ModelChoiceField(queryset=Lifebusinessplans.objects.filter(deleted=False), label=" Select Life Plan: ",
                                      required=False)
    generalPlan = forms.ModelChoiceField(queryset=Generalbusinessplans.objects.filter(deleted=False), label=" Select General Plan: ",
                                         required=False)


# Dates Form, used in Reports section to select particular period's results
class DatesForm(forms.Form):
    date1 = forms.DateField(widget=extras.SelectDateWidget(years=DOY), initial=datetime.now(), label="Date 1")
    date2 = forms.DateField(widget=extras.SelectDateWidget(years=DOY), initial=datetime.now(), label="Date 2")


# Activity Form, used in combination with the CalendarForm to enter a calendar activity
class ActivityForm(forms.ModelForm):
    ORDER = 'activityname', 'customerid', 'date', 'time', 'duration','meeting_minutes'

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        fields = OrderedDict()
        for key in self.ORDER:
            fields[key] = self.fields.pop(key)
        self.fields = fields

    class Meta:
        model = Activity
        fields = {'activityname', 'customerid', 'date', 'time', 'duration','meeting_minutes'}

        labels = {'date': 'Date',
                  'time': 'Time',
                  'duration': 'Duration (in minutes)',
                  'activityname': 'Name',
                  'customerid': 'Related Person',
                  'meeting_minutes': 'Meeting Minutes',
                  }


# Calendar Form, used in combination with the ActivityFrom to enter a calendar activity
class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = {'employee'}
        labels = {'employee': 'Employee'}


# Renewal From, used to renew a contract for a period
class renewalPeriodForm(forms.Form):
    CHOICES = [(3, '3 months'),
               (6, '6 months'),
               (9, '9 months'),
               (12, '1 Year'), ]

    period = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=False)
    other = forms.CharField(required=False)
