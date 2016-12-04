from __future__ import division
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render,redirect
from reportlab.pdfgen import canvas
import random
from datetime import datetime, timedelta
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
        numOfLeadsPerIntroducer[introducer] = 0
        numOfSuccLeadsPerIntroducer[introducer]=0
        clientsFromThisIntroducer = Person.objects.filter(leadfrom=introducer.idperson)
        # Calculate
        for person in clientsFromThisIntroducer:
            numOfLeadsPerIntroducer[introducer]+=1
            if person.isclient == 1:
                numOfSuccLeadsPerIntroducer[introducer]+=1

    #Calculate successful PERCENTAGE for each introducer
        # Where successful PERCENTAGE is ((leads-successfulLeads)/leads)*100
    #Create a list with introducers who have successful percentage over 70%
    successfulPercentage={}
    successfulIntroducers ={}
    for introducer in introducers:
        if numOfLeadsPerIntroducer[introducer]>0:
            percentage=numOfSuccLeadsPerIntroducer[introducer]/numOfLeadsPerIntroducer[introducer]*100.0
            successfulPercentage[introducer]= percentage
        else:
            successfulPercentage[introducer]=0
        if successfulPercentage[introducer]>50:
            successfulIntroducers[introducer]=successfulPercentage[introducer]

    succPercenSorted = OrderedDict(sorted(successfulIntroducers.items(), key=lambda v: v[1], reverse=True))

    #Calculate profit gained from each lead given from introducer
    profits={}
    generalContracts=GeneralContract.objects.all()
    lifeContracts=LifeContract.objects.all()
    for introducer in introducers:
        profits[introducer]=0
    for introducer in introducers:
        clientsFromThisIntroducer = Person.objects.filter(isclient='1', leadfrom=introducer.idperson)
        for person in clientsFromThisIntroducer:
            # General Business profits from this introducer
            genContracts= generalContracts.filter(client = person.idperson)
            if genContracts:
                for contract in genContracts:
                    profit = 0
                    for plan in contract.plan.all():
                        profit += (contract.annualpremium * plan.commission)
                    profits[introducer] += profit

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
                    profits[introducer] += profit

        profitBasedSorted = OrderedDict(sorted(profits.items(),key=lambda x:x[1], reverse=True))

    return render(request, 'leadsMasterApp/iconicIntroducer.html', {'successfulPercentage':successfulPercentage,'introducers':introducers,'succPercenSorted': succPercenSorted,'profitBasedSorted':profitBasedSorted})


