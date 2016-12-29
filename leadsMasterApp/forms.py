from django.db import models
from django.forms import ModelForm,extras
from django import forms
from leadsMasterApp.models import Person, UserProfile,Lifebusinessplans,Generalbusinessplans, LifeContract,GeneralContract,Company
from django.contrib.auth.models import User
from django import forms
from datetime import datetime

DOY = ('1926', '1927', '1928', '1929', '1930', '1931', '1932', '1933', '1934', '1935', '1936', '1937',
       '1938', '1939', '1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949',
       '1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960',
       '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972',
       '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984',
       '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
       '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
       '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017')


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
        fields = ('website', 'employeeid','position','salary','hourspermonth')
        labels = {
            "website": "Website",
            "employeeid": "Employee ID",
            'position': 'Position',
            'salary': 'Salary',
            'hourspermonth': 'Working Hours Per Month'
        }
class PersonForm(forms.ModelForm):

    dateofbirth = forms.DateField(label='Date Of Birth  ',widget=extras.SelectDateWidget(years = DOY))
    class Meta:
        model = Person
        fields = ['idperson','name', 'surname','telephone', 'email','dateofbirth','isclient','isintroducer', 'leadfrom','wasclient']
        labels = {
            "idperson": "Person ID",
            "name": "Name",
            'surname': 'Surname',
            'telephone': 'Telephone',
            'email': 'Email',
            'dateofbirth': 'Date Of Birth',
            'isclient': 'Is Client?',
            'isintroducer': 'Is Introducer?',
            'leadfrom': 'Lead From Person: ',
            'wasclient': 'Was Client ?'
        }

class LifeContractForm(forms.ModelForm):
    issuedate = forms.DateField(widget=extras.SelectDateWidget(years = DOY),initial=datetime.now())
    expirationdate = forms.DateField(widget=extras.SelectDateWidget(years = DOY),initial=datetime.now())
    nextpayment = forms.DateField(widget=extras.SelectDateWidget(years = DOY),initial=datetime.now())

    class Meta:
        model = LifeContract
        fields = ['idcontract','client','issuedate','expirationdate','plan',
                'annualpremium', 'doses','nextpayment', 'price','notes']
        labels = {
            'idcontract':'Contract ID',
            'client': 'Client',
            'issuedate': 'Issue Date',
            'expirationdate': 'Expiration Date',
            'plan': 'Plans Included',
            'annualpremium': 'Annual Premium',
            'doses': 'Payment Doses',
            'nextpayment': 'Next Payment Due',
            'price': 'Total Cost',
            'notes': 'Comments'
        }

class GeneralContractForm(forms.ModelForm):
    issuedate = forms.DateField(widget=extras.SelectDateWidget(years = DOY),initial=datetime.now())
    expirationdate = forms.DateField(widget=extras.SelectDateWidget(years = DOY),initial=datetime.now())
    nextpayment = forms.DateField(widget=extras.SelectDateWidget(years = DOY),initial=datetime.now())

    class Meta:
        model = GeneralContract
        fields = ['idcontract','client','issuedate','expirationdate','plan',
                'annualpremium', 'doses','nextpayment', 'price','notes']
        labels = {
            'idcontract':'Contract ID',
            'client': 'Client',
            'issuedate': 'Issue Date',
            'expirationdate': 'Expiration Date',
            'plan': 'Plans Included',
            'annualpremium': 'Annual Premium',
            'doses': 'Payment Doses',
            'nextpayment': 'Next Payment Due',
            'price': 'Total Cost',
            'notes': 'Comments'
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = {'idcompany','name'}
        labels = {
            'idcompany': 'Company ID',
            'name': 'Name'
        }

class GeneralPlansForm(forms.ModelForm):
    class Meta:
        model = Generalbusinessplans
        fields = {'planid','name','company','commission'}
        labels = {
            'planid': 'Plan ID',
            'name': 'Name',
            'company':'Company Related',
            'commission':'Comission For This Plan'
        }

class LifePlansForm(forms.ModelForm):
    class Meta:
        model = Lifebusinessplans
        fields = {'planlifeid','name','company','firstyearcommission',
                  'maxpercentage','minpercentage','futureprofit','futureprofit2',
                  'futureprofit3','futureprofit4','agelimit','duration'}
        labels = {'planlifeid': 'Plan ID',
                  'name': 'Name',
                  'company':'Company Related',
                  'firstyearcommission': 'First Year Commission',
                  'maxpercentage': 'Maximum Commission Percentage',
                  'minpercentage': 'Minimum Commission Percentage',
                  'futureprofit':'Profit For Future/Second Year',
                  'futureprofit2':'Profit For Third Year (If applicable)',
                  'futureprofit3': 'Profit For Fourth Year (If applicable)',
                  'futureprofit4': 'Profit For Fourth Year (If applicable)',
                  'agelimit': 'Age Limit of Plan',
                  'duration': 'Duration of plan'}

class SearchForm(forms.Form):
    searchbox= forms.CharField(label='Search: ')

