import django_tables2 as tables
from .models import Person,GeneralContract, Generalbusinessplans

class PersonTable(tables.Table):
    class Meta:
        model = Person
        #add class="paleblue" to <table> tag
        fields = ('name', 'surname ')
        attrs = {'class': 'paleblue'}

