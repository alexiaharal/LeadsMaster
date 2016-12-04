from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render,redirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
import random
from datetime import datetime, timedelta
from django.views import generic
from django_tables2 import RequestConfig
from .tables import PersonTable
from .models import Calendar, Person, Activity, GeneralContract, LifeContract
from django.template.context_processors import csrf
import re
from .forms import PersonForm
from collections import OrderedDict

today = datetime.now()

# Create your views here.
def IndexView(request):
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
    for contract in GeneralContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Generalsales.append(contract)
        totalGeneralSales += contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Lifesales.append(contract)
        totalLifeSales += contract.annualpremium
    return render(request, 'leadsMasterApp/index.html',
                  {'renewals':renewals,'activities':activities ,
                   'birthdays':birthdays, 'lifesales':Lifesales ,
                   'generalsales':Generalsales,
                   'totalGeneralSales':totalGeneralSales ,
                   'totalLifeSales':totalLifeSales})

def IndexToDoView(request):
    #Gather activities/to do's for current day
    activities=[]
    for a in Activity.objects.filter(datetime__date=today.date()):
        activities.append(a)
    # Gather sales this day last year
    Generalsales = []
    Lifesales = []
    totalGeneralSales=0
    totalLifeSales = 0
    for contract in GeneralContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Generalsales.append(contract)
        totalGeneralSales += contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Lifesales.append(contract)
        totalLifeSales += contract.annualpremium
    return render(request, 'leadsMasterApp/indexToDo.html',
                  {'activities':activities, 'lifesales':Lifesales ,
                   'generalsales':Generalsales,
                   'totalGeneralSales':totalGeneralSales ,
                   'totalLifeSales':totalLifeSales})


def IndexBirthdayView(request):
    #Gather birthdays for current day
    birthdays = []
    for p in Person.objects.filter(dateofbirth__month=today.month, dateofbirth__day=today.day):
        birthdays.append(p)
    #Gather sales this day last year
    Generalsales=[]
    Lifesales=[]
    totalGeneralSales=0
    totalLifeSales = 0
    for contract in GeneralContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Generalsales.append(contract)
        totalGeneralSales += contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Lifesales.append(contract)
        totalLifeSales += contract.annualpremium
    return render(request, 'leadsMasterApp/indexBirthdays.html',
                  {'birthdays':birthdays , 'lifesales':Lifesales ,
                   'generalsales':Generalsales,
                   'totalGeneralSales':totalGeneralSales ,
                   'totalLifeSales':totalLifeSales})

def IndexRenewalsView(request):
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
    for contract in GeneralContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Generalsales.append(contract)
        totalGeneralSales += contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Lifesales.append(contract)
        totalLifeSales += contract.annualpremium
    return render(request, 'leadsMasterApp/indexRenewals.html',
                  {'generalrenewals':generalrenewals ,
                   'liferenewals':liferenewals,'lifesales':Lifesales ,
                   'generalsales':Generalsales, 'totalGeneralSales':totalGeneralSales ,
                   'totalLifeSales':totalLifeSales})

def IndexPaymentsView(request):
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
    for contract in GeneralContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Generalsales.append(contract)
        totalGeneralSales += contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Lifesales.append(contract)
        totalLifeSales += contract.annualpremium
    return render(request, 'leadsMasterApp/indexPayments.html',
                  {'generalpayments':generalpayments,'lifepayments':lifepayments ,
                   'lifesales':Lifesales , 'generalsales':Generalsales,
                   'totalGeneralSales':totalGeneralSales ,'totalLifeSales':totalLifeSales})

def IndexLeadsToContactView(request):
    # Choose 10 random records to show
    result_entities = []
    for p in Person.objects.raw('SELECT * FROM leadsMasterApp_Person WHERE isclient=0 ORDER BY RANDOM() LIMIT 10'):
        result_entities.append(p)

    #Gather sales this day last year
    Generalsales=[]
    Lifesales=[]
    totalGeneralSales=0
    totalLifeSales = 0
    for contract in GeneralContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Generalsales.append(contract)
        totalGeneralSales += contract.annualpremium
    for contract in LifeContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Lifesales.append(contract)
        totalLifeSales += contract.annualpremium
    return render(request, 'leadsMasterApp/indexLeadsToContact.html',
                  {'lifesales':Lifesales ,
                   'generalsales':Generalsales,
                   'totalGeneralSales':totalGeneralSales ,
                   'totalLifeSales':totalLifeSales,
                   'result_entities':result_entities})

def CalendarView(request):
    output=Calendar.objects.all()
    return render(request, 'leadsMasterApp/calendar.html', {'output':output })

def OurPeopleView(request):
    people=[]
    for p in Person.objects.raw('SELECT * FROM leadsMasterApp_Person ORDER BY RANDOM() LIMIT 10'):
        people.append(p)
    return render(request, 'leadsMasterApp/ourPeople.html', {'people':people})

def AddProfileView(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.save()
            return redirect('ourPeople')
    else:
        form = PersonForm()
    return render(request, 'leadsMasterApp/addProfile.html', {'form':form})

def EditProfileView(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
            form = PersonForm(request.POST, instance=person)
            if form.is_valid():
                person = form.save(commit=False)
                person.save()
                return redirect('ourPeople')
    # elif request.method == 'POST' and request.POST.get('name')=='deleteBtn':
    #         form = PersonForm(request.POST, instance=person)
    #         if form.is_valid():
    #             person = form.save(commit=False)
    #             person.delete()
    #             return redirect('ourPeople')
    else:
        form = PersonForm(instance=person)
    return render(request, 'leadsMasterApp/addProfile.html', {'form': form})


def ReportsView(request):
    table = Person.objects.all()
    return render(request, 'leadsMasterApp/reports.html', {'table':table })

def IconicIntroducerView(request):
    introducers=Person.objects.filter(isintroducer=True)

    # Calculate number of leads and number of successful leads (leads that are current clients) given from each person
    numOfLeadsPerIntroducer ={}
    numOfSuccLeadsPerIntroducer={}
    for introducer in introducers:
        # Initialise dictionaries for both leads and successful leads
        numOfLeadsPerIntroducer[introducer.idperson] = 0
        numOfSuccLeadsPerIntroducer[introducer.idperson]=0
        # Calculate
        for person in Person.objects.all():
            if person.leadfrom == introducer.idperson:
                numOfLeadsPerIntroducer[introducer.idperson]+=1
            if person.isclient == True:
                numOfSuccLeadsPerIntroducer[introducer.idperson]+=1

    #Calculate successful PERCENTAGE for each introducer
        # Where successful PERCENTAGE is ((leads-successfulLeads)/leads)*100
    #Create a list with introducers who have successful percentage over 70%
    successfulPercentage={}
    successfulIntroducers ={}
    for introducer in introducers:
        if numOfLeadsPerIntroducer[introducer.idperson]>0:
            successfulPercentage[introducer.idperson]= ((numOfLeadsPerIntroducer[introducer.idperson]-numOfSuccLeadsPerIntroducer[introducer.idperson])/numOfLeadsPerIntroducer[introducer.idperson])*100
        else:
            successfulPercentage[introducer.idperson]=0
        if successfulPercentage[introducer.idperson]>70:
            successfulIntroducers[introducer]=successfulPercentage[introducer.idperson]

    succPercenSorted = OrderedDict(sorted(successfulIntroducers.items(), key=lambda v: v, reverse=True))

    #Calculate profit gained from each lead given from introducer
    profits={}
    generalContracts=GeneralContract.objects.all()
    lifeContracts=LifeContract.objects.all()
    for introducer in introducers:
        profits[introducer.idperson]=0
    for introducer in introducers:
        clientsFromThisIntroducer = Person.objects.filter(isclient=True, leadfrom=introducer.idperson)
        for person in clientsFromThisIntroducer:
            # General Business profits from this introducer
            genContracts= generalContracts.filter(client = person.idperson)
            if genContracts:
                for contract in genContracts:
                    profit = 0
                    for plan in contract.plan.all():
                        profit += (contract.annualpremium * plan.commission)
                    profits[introducer.idperson] += profit

            # Life Business profits from this introducer
            lifeContr = lifeContracts.filter(client = person.idperson)
            if lifeContr:
                for contract2 in lifeContr:
                    yearOfContract=contract2.issuedate.year - today.year
                    profit =0
                    firstyear = 0
                    nextyears = 0
                    for plan in contract2.plan.all():
                        #get profit for first year of the contract
                        if plan.duration :
                            percentage= plan.duration *plan.firstyearcommission
                        elif (contract2.futureprofit2 or contract2.futureprofit3 or contract2.futureprofit4):
                            percentage = plan.futureprofit
                        else:
                            percentage = (contract2.agelimit - (today - person.dateofbirth).years) * plan.firstyearcommission
                        if percentage <plan.minpercentage:
                            percentage = plan.minpercentage
                        elif percentage > plan.maxpercentage:
                            percentage = plan.maxprcentage
                        firstyear += contract2.annualpremium * percentage

                        #if current contract is issued for more than one year
                        # get profit for the rest of the years up to now
                        if yearOfContract>0:
                            if (contract2.futureprofit2 or contract2.futureprofit3 or contract2.futureprofit4):
                                if yearOfContract==1:
                                    nextyears += contract2.annualpremium*plan.futureprofit2
                                elif yearOfContract==2:
                                    nextyears += (plan.futureprofit3 *contract2.annualpremium) + (plan.futureprofit2 *contract2.annualpremium)
                                else:
                                    nextyears += (plan.futureprofit3 * contract2.annualpremium) + (plan.futureprofit2 * contract2.annualpremium)+(plan.futureprofit2 * contract2.annualpremium *(yearOfContract-2))
                            else:
                                nextyears += plan.futureprofit*yearOfContract *contract2.annualpremium

                    # sum up profit from this contract
                    profit = firstyear + nextyears
                    profits[introducer.idperson] += profit

        profitBasedSorted = OrderedDict(sorted(profits.items(), key=lambda v: v, reverse=True))

    return render(request, 'leadsMasterApp/iconicIntroducer.html', {'succPercenSorted': succPercenSorted,'profitBasedSorted':profitBasedSorted})


