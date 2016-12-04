from django.db import models
from django.forms import ModelForm,extras
from django import forms
from leadsMasterApp.models import Person, Employee
from django.contrib.auth.models import User
from django import forms
class PersonForm(forms.ModelForm):
    DOY = ('1926','1927','1928','1929','1930','1931','1932','1933','1934','1935','1936','1937',
           '1938','1939','1940','1941','1942','1943','1944','1945','1946','1947','1948','1949',
           '1950','1951','1952','1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960',
           '1961','1962','1963','1964', '1965', '1966', '1967','1968','1969','1970','1971','1972',
           '1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984',
           '1985','1986','1987','1988','1989','1990','1991', '1992', '1993', '1994', '1995',
           '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003','2004', '2005', '2006',
           '2007', '2008', '2009', '2010', '2011','2012', '2013', '2014', '2015', '2016','2017')
    idperson = forms.IntegerField(label='ID')
    name = forms.CharField(label='Name ',max_length = 50)
    surname = forms.CharField(label='Surname  ',max_length = 50)
    telephone = forms.CharField(label='Telephone  ',max_length = 15)
    email = forms.CharField(label='Email  ',max_length = 45,required=False)
    dateofbirth = forms.DateField(label='Date Of Birth  ',widget=extras.SelectDateWidget(years = DOY))
    isclient = forms.ChoiceField(choices=Person.client_CHOICES,label="Is Client  ")
    isintroducer = forms.ChoiceField(choices=Person.introducer_CHOICES, label='Is Introducer  ')
    leadfrom = forms.IntegerField(label='Lead from person with ID  ')

    class Meta:
        model = Person
        fields = ['idperson','name', 'surname','telephone', 'email','dateofbirth','isclient','isintroducer', 'leadfrom']

