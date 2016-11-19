from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render
from django.template import loader
from django.http import Http404
from django.urls import reverse
from datetime import datetime, timedelta
from django.views import generic
from django_tables2 import RequestConfig
from .tables import PersonTable
from .models import Calendar, Person, Activity, GeneralContract, LifeContract

# Create your views here.

def IndexView(request):
    today=datetime.now()
    #Gather all activities for current day
    activities=[]
    for a in Activity.objects.filter(datetime__date=today.date()):
        activities.append(a)
    #Gather birthdays for current day
    birthdays = []
    for p in Person.objects.filter(dateofbirth__month=today.month, dateofbirth__day=today.day):
        birthdays.append(p)
    #Gather renewals for current day
    renewals = []
    for contract in GeneralContract.objects.filter(expirationdate__date=today.date()):
        renewals.append(contract)
    #Gather sales this day last year
    Generalsales=[]
    Lifesales=[]
    totalGeneralSales=0
    totalLifeSales = 0
    for contract in GeneralContract.objects.filter(issuedate__day = today.day,issuedate__month= today.month,issuedate__year = (today.year-1)):
        Generalsales.append(contract)
        totalGeneralSales +=contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day = today.day,issuedate__month = today.month,issuedate__year = (today.year-1)):
        Lifesales.append(contract)
        totalLifeSales +=contract.annualpremium
    return render(request, 'leadsMasterApp/index.html', {'renewals':renewals,'activities':activities ,'birthdays':birthdays, 'lifesales':Lifesales , 'generalsales':Generalsales, 'totalGeneralSales':totalGeneralSales ,'totalLifeSales':totalLifeSales})

def IndexToDoView(request):
    today=datetime.now()
    #Gather activities/to do's for current day
    activities=[]
    for a in Activity.objects.filter(datetime__date=today.date()):
        activities.append(a)
    # Gather sales this day last year
    Generalsales = []
    Lifesales = []
    totalGeneralSales=0
    totalLifeSales = 0
    for contract in GeneralContract.objects.filter(issuedate__day = today.day,issuedate__month= today.month,issuedate__year = (today.year-1)):
        Generalsales.append(contract)
        totalGeneralSales +=contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day = today.day,issuedate__month = today.month,issuedate__year = (today.year-1)):
        Lifesales.append(contract)
        totalLifeSales +=contract.annualpremium
    return render(request, 'leadsMasterApp/indexToDo.html', {'activities':activities, 'lifesales':Lifesales , 'generalsales':Generalsales, 'totalGeneralSales':totalGeneralSales ,'totalLifeSales':totalLifeSales})


def IndexBirthdayView(request):
    today=datetime.now()
    #Gather birthdays for current day
    birthdays = []
    for p in Person.objects.filter(dateofbirth__month=today.month, dateofbirth__day=today.day):
        birthdays.append(p)
    #Gather sales this day last year
    Generalsales=[]
    Lifesales=[]
    totalGeneralSales=0
    totalLifeSales = 0
    for contract in GeneralContract.objects.filter(issuedate__day = today.day,issuedate__month= today.month,issuedate__year = (today.year-1)):
        Generalsales.append(contract)
        totalGeneralSales +=contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day = today.day,issuedate__month = today.month,issuedate__year = (today.year-1)):
        Lifesales.append(contract)
        totalLifeSales +=contract.annualpremium
    return render(request, 'leadsMasterApp/indexBirthdays.html', {'birthdays':birthdays , 'lifesales':Lifesales , 'generalsales':Generalsales, 'totalGeneralSales':totalGeneralSales ,'totalLifeSales':totalLifeSales})

def IndexRenewalsView(request):
    today=datetime.now()
    #Gather renewals for current day
    generalrenewals = []
    for contract in GeneralContract.objects.filter(expirationdate__date=today.date()):
        generalrenewals.append(contract)
    liferenewals = []
    for contract in LifeContract.objects.filter(expirationdate__date=today.date()):
        liferenewals.append(contract)
    #Gather sales this day last year
    Generalsales=[]
    Lifesales=[]
    totalGeneralSales=0
    totalLifeSales = 0
    for contract in GeneralContract.objects.filter(issuedate__day = today.day,issuedate__month= today.month,issuedate__year = (today.year-1)):
        Generalsales.append(contract)
        totalGeneralSales +=contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day = today.day,issuedate__month = today.month,issuedate__year = (today.year-1)):
        Lifesales.append(contract)
        totalLifeSales +=contract.annualpremium
    return render(request, 'leadsMasterApp/indexRenewals.html', {'generalrenewals':generalrenewals , 'liferenewals':liferenewals,'lifesales':Lifesales , 'generalsales':Generalsales, 'totalGeneralSales':totalGeneralSales ,'totalLifeSales':totalLifeSales})

def IndexPaymentsView(request):
    today=datetime.now()
    #Gather renewals for current day
    generalpayments = []
    for contract in GeneralContract.objects.filter(nextpayment__date=today.date()):
        generalpayments.append(contract)
    lifepayments = []
    for contract in GeneralContract.objects.filter(nextpayment__date=today.date()):
        lifepayments.append(contract)
    #Gather sales this day last year
    Generalsales=[]
    Lifesales=[]
    totalGeneralSales=0
    totalLifeSales = 0
    for contract in GeneralContract.objects.filter(issuedate__day = today.day,issuedate__month= today.month,issuedate__year = (today.year-1)):
        Generalsales.append(contract)
        totalGeneralSales +=contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day = today.day,issuedate__month = today.month,issuedate__year = (today.year-1)):
        Lifesales.append(contract)
        totalLifeSales +=contract.annualpremium
    return render(request, 'leadsMasterApp/indexPayments.html', {'generalpayments':generalpayments,'lifepayments':lifepayments , 'lifesales':Lifesales , 'generalsales':Generalsales, 'totalGeneralSales':totalGeneralSales ,'totalLifeSales':totalLifeSales})


def CalendarView(request):
    output=Calendar.objects.all()
    return render(request, 'leadsMasterApp/calendar.html', {'output':output })

def OurPeopleView(request):
    table = PersonTable(Person.objects.all())
    return render(request, 'leadsMasterApp/ourPeople.html', {'table':table })

def ReportsView(request):
    table = PersonTable(Person.objects.all())
    return render(request, 'leadsMasterApp/reports.html', {'table':table })



"""
class ActivityView(generic.DetailView):
    model = Calendar
    template_name = 'leadsMasterApp/detail.html'

def add_entry(request, entryid):
    entry = get_object_or_404(Calendar,pk=entryid)
    try:
        selected_field = entry.activity_set.get(pk=request.POST['field'])
    except (KeyError, Activity.DoesNotExist):
        return render(request, 'leadsMasterApp/detail.html',
                      {'field': entry.activity_set.activityname,'error_message': "You didn't select a field.",
                                                        })
    else:
        selected_field.activityname = "kati"
        selected_field.save()
        return HttpResponseRedirect(reverse('results',args=(entryid,)))


def index(request):
    #output = Calendar.objects.raw('SELECT entryID, activity FROM Calendar')
    output = Calendar.objects.all()
    template = loader.get_template('leadsMasterApp/index.html')
    context = {'output': output,}

    return render(request, 'leadsMasterApp/index.html',context)

def activity(request, entryid):
    activity = get_object_or_404(Calendar, pk=entryid)
    return render (request, 'leadsMasterApp/detail.html',{'activity':activity})

def add_entry(request, entryid):
    entry = get_object_or_404(Calendar,pk=entryid)
    try:
        selected_field = entry.activity_set.get(pk=request.POST['field'])
    except (KeyError, Activity.DoesNotExist):
        return render(request, 'leadsMasterApp/detail.html',
                      {'field': activity,'error_message': "You didn't select a field.",
                                                        })
    else:
        selected_field.activityname = "kati"
        selected_field.save()
        return HttpResponseRedirect(reverse('results',args=(entryid,)))
"""