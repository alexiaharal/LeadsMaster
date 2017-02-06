from __future__ import division

from calendar import monthrange

from django.shortcuts import render, get_object_or_404,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.template.context import RequestContext
from datetime import datetime, timedelta, date, time

from django.conf import settings
from .models import Calendar, Person, Activity, GeneralContract, LifeContract,Company, Generalbusinessplans, \
    Lifebusinessplans, birthdayNot, genRenewalsNot, lifeRenewalsNot, genPaymentsNot, lifePaymentsNot
from django.db.models import Q
from django.core.mail import send_mail

from .forms import SearchForm, PersonForm, LifeContractForm, CompanyForm,GeneralPlansForm,LifePlansForm, GeneralContractForm, UserForm, UserProfileForm, \
    ActivityForm, CalendarForm, DatesForm, PlansOptionsForm, renewalPeriodForm
from collections import OrderedDict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta

#####----- Views -----######

today = datetime.now()

def register(request):
    # get the request's context.
    context = RequestContext(request)

    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            # Save the user's form data to the database.
            user = user_form.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            # Now we save the UserProfile model instance.
            profile.save()

            #tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'leadsMasterApp/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None, no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # send the user back to the homepage.
                login(request, user)
                return redirect('index')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request,'leadsMasterApp/login.html', {}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return redirect('login')


actEmails = {}

def IndexView(request):
    today = datetime.now()

    #Gather all activities for current day
    activities=[]
    for a in Activity.objects.filter(date=today.date()):
        activities.append(a)

        if a.customerid.email:
            if a.email == False:
                # insert code here to send email if you want to
                a.email = True
                a.save()

    #Gather birthdays for current day
    birthdays = []
    emails = []

    for p in Person.objects.filter(dateofbirth__month=today.month, dateofbirth__day=today.day):
        birthdays.append(p)
        birthdayTable = birthdayNot.objects.all()

        if birthdayTable.filter(birthday=p, date=today.date()).exists():
            flag=True
        else:
            if p.email:
                emails.append(p.email)
                obj = birthdayNot(birthday=p, date=today.date(),email=True)
                obj.save()
    if emails:
        send_mail(
            'Happy Birthday',
            'Leads Master system, on behalf of your insurance agent, wishes you a very happy birthday.',
            settings.EMAIL_HOST_USER,
            emails
        )


    #Gather renewals for current day
    generalrenewals = []
    for contract in GeneralContract.objects.filter(expirationdate=today.date(),cancelled=False):
        generalrenewals.append(contract)
        genRenTable = genRenewalsNot.objects.all()
        if genRenTable.filter(renewal=contract, date=today.date()).exists():
            flag = True
        else:
            if contract.client.email:
                plans=""
                for p in contract.plan.all():
                    plans+= str(p)
                text='This is a reminder that your ' + plans + ' contract, with contract number: '+ str(contract.idcontract)+ ' is expiring today! Please get in touch to renew. Thank you, Leads Master'
                send_mail(
                    'Contract Renewal Reminder',
                    text,
                    settings.EMAIL_HOST_USER,
                    [contract.client.email]
                )
                obj = genRenewalsNot(renewal=contract, date=today.date(),email=True)
                obj.save()




    liferenewals = []
    for contract in LifeContract.objects.filter(expirationdate=today.date(),cancelled=False):
        liferenewals.append(contract)
        lifeRenTable = lifeRenewalsNot.objects.all()
        if lifeRenTable.filter(renewal=contract, date=today.date()).exists():
            flag = True
        else:
            if contract.client.email:
                plans=""
                for p in contract.plan.all():
                    plans+= str(p)
                text='This is a reminder that your ' +plans+ ' contract, with contract number: '+ str(contract.idcontract)+ ' is expiring today! If you dont\' want it to be renewed please get in touch. Thank you, Leads Master'
                send_mail(
                    'Contract Renewal Notification',
                    text,
                    settings.EMAIL_HOST_USER,
                    [contract.client.email]
                )
                obj = lifeRenewalsNot(renewal=contract, date=today.date(),email=True)
                obj.save()


    #Gather payments for current day
    generalpayments = []
    for contract in GeneralContract.objects.filter(nextpayment=today.date(),cancelled=False):
        generalpayments.append(contract)
        genPaymTable = genPaymentsNot.objects.all()
        if genPaymTable.filter(payment=contract, date=today.date()).exists():
            flag = True
        else:
            if contract.client.email:
                plans=""
                for p in contract.plan.all():
                    plans+= str(p)
                text='This is a reminder that your ' +plans+ ' contract, with contract number: '+ str(contract.idcontract)+ ' needs to be paid! Please get in touch to arrange a meeting. Thank you, Leads Master'
                print contract.client.email
                send_mail(
                    'Contract Payment Reminder',
                    text,
                    settings.EMAIL_HOST_USER,
                    [contract.client.email]
                )
                obj = genPaymentsNot(payment=contract, date=today.date(),email=True)
                obj.save()

    lifepayments = []
    for contract in LifeContract.objects.filter(nextpayment=today.date(),cancelled=False):
        lifepayments.append(contract)
        lifePaymTable = lifePaymentsNot.objects.all()
        if lifePaymTable.filter(payment=contract, date=today.date()).exists():
            flag = True
        else:
            if contract.client.email:
                plans=""
                for p in contract.plan.all():
                    plans+= str(p)
                text='This is a reminder that your ' +plans+ ' contract, with contract number: '+ str(contract.idcontract)+ ' needs to be paid! Please get in touch to arrange a meeting. Thank you, Leads Master'
                send_mail(
                    'Contract Payment Reminder',
                    text,
                    settings.EMAIL_HOST_USER,
                    [contract.client.email]
                )
                obj = lifePaymentsNot(payment=contract, date=today.date(), email=True)
                obj.save()


    # Automatically renew Life contracts
    yesterday= today- timedelta(1)
    for contract in LifeContract.objects.filter(expirationdate__lt=today.date(),cancelled=False):
        c=contract
        newDate= c.expirationdate + relativedelta(years=+1)
        c.expirationdate =newDate
        c.save()

    #Gather sales this day last year
    Generalsales=[]
    Lifesales=[]
    totalGeneralSales=0
    totalLifeSales = 0
    # Choose 10 random records to show
    if today.weekday()==0:
        result_entities = []
        for p in Person.objects.raw('SELECT * FROM leadsMasterApp_Person WHERE isclient=0 ORDER BY RANDOM() LIMIT 10'):
            result_entities.append(p)
    else:
        result_entities=[]
    #Calculate Sales Past Years This Day
    for contract in GeneralContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Generalsales.append(contract)
        totalGeneralSales += contract.annualpremium

    for contract in LifeContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
        Lifesales.append(contract)
        totalLifeSales += contract.annualpremium


    return render(request, 'leadsMasterApp/indexBase.html',
                  {'generalrenewals':generalrenewals,'generalpayments':generalpayments,
                   'activities':activities , 'birthdays':birthdays, 'lifesales':Lifesales ,
                   'generalsales':Generalsales,'totalGeneralSales':totalGeneralSales ,
                   'liferenewals':liferenewals, 'lifepayments':lifepayments,
                   'totalLifeSales':totalLifeSales,
                   'result_entities': result_entities})


def calendar(request,day=None,month=None,year=None):
    today = datetime.now()

    calendarEntries=Calendar.objects.all()
    if day is None:
        day=today.date().day
        month=today.date().month
        year = today.date().year


    dailyEntries= Calendar.objects.filter(activity__date__day=day,activity__date__month=month,activity__date__year=year)
    if request.method == "POST":
        form1 = ActivityForm(request.POST)
        form2 = CalendarForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            activity = form1.save(commit=False)
            activity.save()

            calendar = form2.save(commit=False)
            employee= form2.cleaned_data['employee']
            calendarEntry= Calendar(activity=activity,employee=employee)
            calendarEntry.save()
            return redirect('calendar')
    else:
        form1 = ActivityForm()
        form2 = CalendarForm()

    return render(request,'leadsMasterApp/calendar.html',{'day':day,'month':month,'year':year,'calendarEntries':calendarEntries,'dailyEntries':dailyEntries,'form1':form1,'form2': form2})


def successfulLeadsPercentage(introducer):
    numOfLeads = 0
    numOfSuccLeads = 0
    leadsFromIntroducer = Person.objects.filter(leadfrom=introducer.id)
    # Calculate
    for person in leadsFromIntroducer:
        numOfLeads += 1
        if person.isclient == 1:
            numOfSuccLeads += 1
    #Calculate successful PERCENTAGE
        # Where successful PERCENTAGE is ((leads-successfulLeads)/leads)*100
    successfulPercentage=0
    successfulIntroducers ={}
    if numOfSuccLeads>0:
        percentage=numOfSuccLeads/numOfLeads*100.0
    else:
        percentage=0
    percentage=float("{0:.2f}".format(percentage))

    return percentage

def OurPeopleView(request):
    query=""
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['searchbox']
    else:
        form=SearchForm()

    if query!="":
        people=[]
        for p in Person.objects.filter( Q(name__startswith=query)):
           if p not in people:
               people.append(p)
        for p in Person.objects.filter(Q(surname__startswith=query)):
           if p not in people:
               people.append(p)
        for p in Person.objects.filter(Q(idperson__startswith=query)):
           if p not in people:
               people.append(p)
    else:
        people=[]
        for p in Person.objects.raw('SELECT * FROM leadsMasterApp_Person '):
            people.append(p)
    return render(request, 'leadsMasterApp/ourPeople.html', {'form':form,'people':people})

def ManHoursView(request):
    query=""
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['searchbox']
    else:
        form=SearchForm()

    if query!="":
        people=[]
        for p in Person.objects.filter( Q(name__startswith=query)):
           if p not in people:
               people.append(p)
        for p in Person.objects.filter(Q(surname__startswith=query)):
           if p not in people:
               people.append(p)
        for p in Person.objects.filter(Q(idperson__startswith=query)):
           if p not in people:
               people.append(p)
    else:
        people=[]
        for p in Person.objects.raw('SELECT * FROM leadsMasterApp_Person'):
            people.append(p)
    return render(request, 'leadsMasterApp/manHoursBase.html', {'form':form,'people':people})

def ManHoursPersonView(request,pk):
    person= get_object_or_404(Person,pk=pk)
    activities= Calendar.objects.filter(activity__customerid=person).order_by('activity__date')
    totalHours=0
    for a in activities:
        totalHours+= a.activity.duration
    totalHours=totalHours/60
    totalHours=float("{0:.2f}".format(totalHours))
    return render(request, 'leadsMasterApp/manHoursPerson.html', {'person':person,'activities':activities,'totalHours':totalHours})

def SuccLeadsView(request):

    query = ""
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['searchbox']
    else:
        form = SearchForm()

    if query != "":
        introducers=Person.objects.all()
        resultIntroducers = []
        myintroducers={}
        flag=1
        for p in introducers.filter(Q(name__startswith=query)):
            if p not in resultIntroducers:
                resultIntroducers.append(p)
        for p in introducers.filter(Q(surname__startswith=query)):
            if p not in resultIntroducers:
                resultIntroducers.append(p)
        for p in introducers.filter(Q(idperson__startswith=query)):
            if p not in resultIntroducers:
                resultIntroducers.append(p)
        for p in resultIntroducers:
            percentage=successfulLeadsPercentage(p)
            myintroducers[p]=percentage
    else:
        introducers = Person.objects.filter(isintroducer=1)
        topIntroducers = {}
        myintroducers={}
        flag=0
        for p in introducers:
            percentage=successfulLeadsPercentage(p)
            topIntroducers[p]=percentage
            myintroducers = OrderedDict(sorted(topIntroducers.items(), key=lambda x: x[1], reverse=True))

    return render(request, 'leadsMasterApp/succLeads.html', {'form':form,'flag':flag,'myintroducers':myintroducers})

def succLeadsPersonView(request,pk):
    person= get_object_or_404(Person,pk=pk)
    leads = Person.objects.filter(leadfrom=person)
    successfulLeads=leads.filter(isclient=1)
    numOfLeads=len(leads)
    numOfSuccLeads=len(successfulLeads)
    percentage=successfulLeadsPercentage(person)
    return render(request, 'leadsMasterApp/succLeadsPerson.html', {'numOfLeads':numOfLeads,'numOfSuccLeads':numOfSuccLeads,'percentage':percentage,'successfulLeads':successfulLeads,'person':person,'leads':leads})

def salesReportsView(request):
    today = datetime.now()

    date1=""
    date2=""
    lifePlan = ""
    generalPlan=""
    if request.method == "POST":
        form = DatesForm(request.POST)
        plansForm = PlansOptionsForm(data=request.POST)
        if form.is_valid() and plansForm.is_valid():
            date1 = form.cleaned_data['date1']
            date2 = form.cleaned_data['date2']
            generalPlan = plansForm.cleaned_data['generalPlan']
            lifePlan = plansForm.cleaned_data['lifePlan']

    else:
        form = DatesForm()
        plansForm = PlansOptionsForm()

    ###### The difference here of sales and profits reports is that  ########
    ###### dates for sales are the issue dates of the contract (including issue year) ######
    ###### dates for profits are the issue days and months to calculate what profits #######
    ###### the agent is going to gain within that month #####

    if (date1=="") and (date2==""):
        currentGenSales= GeneralContract.objects.filter(issuedate__month=today.month,issuedate__year=today.year,cancelled=False)
        currentLifeSales=LifeContract.objects.filter(issuedate__month=today.month,issuedate__year=today.year,cancelled=False)
        currentGenProfits=GeneralContract.objects.filter(issuedate__month=today.month,cancelled=False)
        currentLifeProfits=LifeContract.objects.filter(issuedate__month=today.month,cancelled=False)
    else:
        currentGenSales = GeneralContract.objects.filter(issuedate__range=[date1, date2],cancelled=False)
        currentLifeSales = LifeContract.objects.filter(issuedate__range=[date1, date2],cancelled=False)
        currentGenProfits = GeneralContract.objects.filter(Q(issuedate__month = date1.month) , Q(issuedate__month = date2.month), Q(issuedate__day__gte= date1.day), Q(issuedate__day__lte = date2.day), cancelled=False)
        currentLifeProfits = LifeContract.objects.filter(Q(issuedate__month = date1.month) , Q(issuedate__month = date2.month), Q(issuedate__day__gte= date1.day), Q(issuedate__day__lte = date2.day),cancelled=False)


    if (lifePlan!="") or (generalPlan!=""):
        if (not lifePlan) and generalPlan:
            currentGenSales = currentGenSales.filter(plan=generalPlan.planid)
            currentLifeSales = {}
            currentGenProfits = currentGenProfits.filter(plan=generalPlan.planid)
            currentLifeProfits = {}
        elif (not generalPlan) and lifePlan:
            currentGenSales = {}
            currentLifeSales =currentLifeSales.filter(plan=lifePlan.planlifeid)
            currentGenProfits = {}
            currentLifeProfits = currentLifeProfits.filter(plan=lifePlan.planlifeid)

    #### Sales Calculations ######
    # Calculate total Annual Premium for General Sales
    totalCurrentAnnualGen=0
    for sale in currentGenSales:
        totalCurrentAnnualGen+= sale.annualpremium

    # Calculate total Annual Premium for General Sales
    totalCurrentAnnualLife=0
    for sale in currentLifeSales:
        totalCurrentAnnualLife+= sale.annualpremium

    #Calculate profits and total profit for General Sales Report
    generalSalesProfits={}
    totalGeneralSalesProfit=0
    for contract in currentGenSales:
        generalSalesProfits[contract]=generalContractProfit(contract)
        totalGeneralSalesProfit+=generalSalesProfits[contract]

    #Calculate profits and total profit for General Profits Report
    generalProfits={}
    totalGeneralProfit=0
    for contract in currentGenProfits:
        generalProfits[contract]=generalContractProfit(contract)
        totalGeneralProfit+=generalProfits[contract]

    # Calculate profits and total profit for Life Sales Report
    totalLifeSalesProfits={}
    totalLifeSalesProfit=0
    for contract in currentLifeSales:
        totalLifeSalesProfits[contract]=lifeContractProfit(contract,contract.client)
        totalLifeSalesProfit+=totalLifeSalesProfits[contract]["thisYearProfit"]

    # Calculate profits and total profit for Life Profits Report
    totalLifeProfits={}
    totalLifeProfit=0
    for contract in currentLifeProfits:
        totalLifeProfits[contract]=lifeContractProfit(contract,contract.client)
        totalLifeProfit+=totalLifeProfits[contract]["thisYearProfit"]

    ###### Profits Calculations #####
    return render(request, 'leadsMasterApp/salesReports.html',{'totalLifeSalesProfits':totalLifeSalesProfits,
        'totalLifeSalesProfit':totalLifeSalesProfit,'totalCurrentAnnualLife':totalCurrentAnnualLife,'form':form,
        'generalSalesProfits':generalSalesProfits,'totalGeneralSalesProfit':totalGeneralSalesProfit,'totalCurrentAnnualGen':totalCurrentAnnualGen,
        'totalLifeProfits':totalLifeProfits,'totalLifeProfit':totalLifeProfit,'generalProfits':generalProfits,
        'totalGeneralProfit':totalGeneralProfit, 'plansForm':plansForm
    })

def generalContractProfit(contract):
    profit=0
    for plan in contract.plan.all():
        profit+= (contract.annualpremium * plan.commission / 100)
    return (profit)

def lifeContractProfit(contract,person):
    today = datetime.now()

    yearsOfContract =relativedelta(today.date(), contract.issuedate).years
    profit = 0
    firstyear = 0
    nextyears = 0
    #get profit from all plans if more than one plan
    for plan in contract.plan.all():
        ## FIRST year profit ##

        # Get percentage
        if (plan.futureprofit2 or plan.futureprofit3 or plan.futureprofit4) :
            percentage = plan.firstyearcommission
        elif contract.duration:
            percentage = contract.duration * plan.firstyearcommission
        else:
            percentage = (plan.agelimit - (relativedelta(today.date(), person.dateofbirth).years )) * plan.firstyearcommission

        #Check if in range of percentages
        if percentage < plan.minpercentage:
            percentage = plan.minpercentage
        elif percentage > plan.maxpercentage:
            percentage = plan.maxpercentage

        # Save First Year's Commission
        firstyear = contract.annualpremium * percentage / 100

        # If current contract is issued for more than one year
        # REST OF THE YEARS profit -  up to now
        if yearsOfContract > 0:
            if (plan.futureprofit2 or plan.futureprofit3 or plan.futureprofit4):
                if yearsOfContract == 1:
                    nextyears += contract.annualpremium * plan.futureprofit2 / 100
                    thisYearProfit=contract.annualpremium *plan.futureprofit2 / 100
                elif yearsOfContract == 2:
                    nextyears += (plan.futureprofit3 /100 * contract.annualpremium) + (
                    plan.futureprofit2 /100 * contract.annualpremium)
                    thisYearProfit=contract.annualpremium*plan.futureprofit3 / 100
                else:
                    nextyears += (plan.futureprofit3 /100 * contract.annualpremium) + (
                        plan.futureprofit2 /100 * contract.annualpremium) + (
                        plan.futureprofit4 /100 * contract.annualpremium * (yearsOfContract - 2))
                    thisYearProfit=plan.futureprofit4 /100
            else:
                nextyears += plan.futureprofit / 100 * yearsOfContract * contract.annualpremium
                thisYearProfit=plan.futureprofit / 100 *contract.annualpremium
        else:
            thisYearProfit=firstyear
    # sum up profit from this contract
    totalProfit = firstyear + nextyears
    profit={}
    totalProfit = float("{0:.2f}".format(totalProfit))
    thisYearProfit=float("{0:.2f}".format(thisYearProfit))
    profit['total']=totalProfit
    profit['thisYearProfit']=thisYearProfit
    return (profit)

def AddProfileView(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            if form.cleaned_data['leadfrom']:
                introducer=Person.objects.get(idperson=form.cleaned_data['leadfrom'].idperson)
                if introducer.isintroducer == 0:
                    introducer.isintroducer = 1
                    introducer.save()
            person.save()
            return redirect('ourPeople')
    else:
        form=PersonForm()
    return render(request, 'leadsMasterApp/addProfile.html', {'form':form})

def EditProfileView(request, pk):
    person = get_object_or_404(Person, pk=pk)
    form = PersonForm(data = request.POST or None, instance=person)
    if form.is_valid():
        person = form.save(commit=False)
        if form.cleaned_data['leadfrom']:
            introducer = Person.objects.get(idperson=form.cleaned_data['leadfrom'].idperson)
            if introducer.isintroducer == 0:
                introducer.isintroducer = 1
                introducer.save()
        person.save()
        return redirect('ourPeople')
    return render(request, 'leadsMasterApp/addProfile.html', {'form': form})

def ProfileView (request, pk):
    person = get_object_or_404(Person, pk=pk)
    generalContracts = GeneralContract.objects.filter(client = person, cancelled=False)
    lifeContracts = LifeContract.objects.filter(client = person, cancelled=False)
    leads = Person.objects.filter(leadfrom=person)
    percentage=successfulLeadsPercentage(person)
    return render(request, 'leadsMasterApp/profile.html',
                  {'person':person , 'generalContracts':generalContracts,
                   'lifeContracts':lifeContracts,'leads':leads,'percentage':percentage})

def ContractPageView(request,pk,type):
    today = datetime.now()

    if type=='life':
        contract=get_object_or_404(LifeContract, pk=pk)
        life=1
        t='life'
        yearsInyears=""
    else:
        contract=get_object_or_404(GeneralContract, pk=pk)
        life=0
        t='general'
        yearsInyears = contract.years /12
        if yearsInyears<1:
            yearsInyears=0
        yearsInyears = float("{0:.2f}".format(yearsInyears))

    person=contract.client
    totalPayment=contract.price
    if contract.nextpayment!="":
        nextPayment=float("{0:.2f}".format(contract.price/contract.doses))
    else:
        nextPayment=""
    expired=0
    if contract.expirationdate < today.date() :
        expired=1

    if request.method == "POST":
        form = renewalPeriodForm(request.POST)
        if form.is_valid() :
            if form.cleaned_data['other'] == "":
                period = form.cleaned_data['period']
            else:
                period = form.cleaned_data['other']
            c = contract
            newExpDate = c.expirationdate + relativedelta(months=+int(period))
            c.years+=int(period)
            c.issuedate = c.expirationdate
            c.expirationdate = newExpDate
            c.save()
            return redirect('contractPage', pk=pk , type=t)
    else:
        form = renewalPeriodForm()
    return render(request, 'leadsMasterApp/contractPage.html',
                  {'contract':contract,'life':life,
                   'person':person,'totalPayment':totalPayment,'yearsInyears':yearsInyears,
                   'nextPayment':nextPayment,'expired':expired, 'form':form})

def addContractLifeView(request):
    if request.method == 'POST':
        contract_form = LifeContractForm(request.POST)
        if contract_form.is_valid():
            profile = contract_form.save(commit=False)
            p = Person.objects.get(idperson=contract_form.cleaned_data['client'].idperson)
            if p.isclient == 0:
                p.isclient = 1
                p.save()
            profile.save()
            contract_form.save_m2m()
            return redirect('ProfileView', pk=p.id)
        else:
            print contract_form.errors
    else:
        contract_form = LifeContractForm()
    return render(request,
                  'leadsMasterApp/addContractLife.html',
                  {'add_contract_form': contract_form})


def editContractLifeView(request, pk):
    instance=get_object_or_404(LifeContract, pk=pk)
    form = LifeContractForm(data = request.POST or None, instance=instance)
    if form.is_valid():
        instance=form.save(commit=False)
        p = Person.objects.get(idperson=form.cleaned_data['client'].idperson)
        if p.isclient == 0:
            p.isclient = 1
            p.save()
        if form.cleaned_data['cancelled']==True:
            p.wasclient=1
            contractsOfPersonLife=LifeContract.objects.filter(client=p, cancelled=False)
            contractsOfPersonGeneral=GeneralContract.objects.filter(client=p,cancelled=False)
            if len(contractsOfPersonGeneral)==0 and len(contractsOfPersonLife)==1:
                p.isclient=0
            p.save()
        instance.save()
        form.save_m2m()
        return redirect ('ProfileView', pk=p.id )

    return render(request,
        'leadsMasterApp/addContractLife.html',
        {'add_contract_form':form})

def addContractGeneralView(request):
    if request.method == 'POST':
        contract_form = GeneralContractForm(request.POST)
        if contract_form.is_valid():
            profile = contract_form.save(commit=False)
            p = Person.objects.get(idperson=contract_form.cleaned_data['client'].idperson)
            if p.isclient == 0:
                p.isclient = 1
                p.save()
            profile.save()
            contract_form.save_m2m()
            return redirect('ProfileView', pk=p.id)
        else:
            print contract_form.errors
    else:
        contract_form = GeneralContractForm()
    return render(request,
            'leadsMasterApp/addContractGeneral.html',
            {'add_contract_form':contract_form})

def editContractGeneralView(request,pk):
    instance = get_object_or_404(GeneralContract, pk=pk)
    form = GeneralContractForm(data=request.POST or None, instance=instance)
    if form.is_valid():
        instance=form.save(commit=False)
        p = Person.objects.get(idperson=form.cleaned_data['client'].idperson)
        if p.isclient == 0:
            p.isclient = 1
            p.save()
        if form.cleaned_data['cancelled']==True:
            p.wasclient=1
            contractsOfPersonLife=LifeContract.objects.filter(client=p, cancelled=False)
            contractsOfPersonGeneral=GeneralContract.objects.filter(client=p,cancelled=False)
            if len(contractsOfPersonGeneral)==1 and len(contractsOfPersonLife)==0:
                p.isclient=0
            p.save()
        instance.save()
        form.save_m2m()
        return redirect('ProfileView', pk=p.id)

    return render(request,
            'leadsMasterApp/addContractGeneral.html',
            {'add_contract_form':form})

def ReportsView(request):
    table = Person.objects.all()
    return render(request, 'leadsMasterApp/reports.html', {'table':table })

def CompaniesView(request):
    companies= Company.objects.all()
    genPlans = Generalbusinessplans.objects.all()
    lifePlans = Lifebusinessplans.objects.all()

    return render(request, 'leadsMasterApp/companies.html', {'companies':companies,'genPlans':genPlans,'lifePlans':lifePlans})

def AddCompanyView(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            return redirect('companies')
    else:
        form=CompanyForm()

    return render(request, 'leadsMasterApp/addCompany.html', {'form':form})

def EditCompanyView(request,pk):
    instance=get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=instance)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            return redirect('companies')
    else:
        form=CompanyForm(instance=instance)

    return render(request, 'leadsMasterApp/addCompany.html', {'form':form})

def AddGenPlanView(request):
    if request.method == "POST":
        form = GeneralPlansForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('companies')
    else:
        form = GeneralPlansForm()

    return render(request, 'leadsMasterApp/addGenPlan.html', {'form':form})

def EditGenPlanView(request,pk):
    instance = get_object_or_404(Generalbusinessplans, pk=pk)
    if request.method == "POST":
        form = GeneralPlansForm(request.POST, instance=instance)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('companies')
    else:
        form = GeneralPlansForm(instance=instance)

    return render(request, 'leadsMasterApp/addGenPlan.html', {'form':form})

def AddLifePlanView(request):
    if request.method == "POST":
        form = LifePlansForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('companies')
    else:
        form = LifePlansForm()

    return render(request, 'leadsMasterApp/addLifePlan.html', {'form':form})

def EditLifePlanView(request,pk):
    instance = get_object_or_404(Lifebusinessplans, pk=pk)
    if request.method == "POST":
        form = LifePlansForm(request.POST, instance=instance)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('companies')
    else:
        form = LifePlansForm(instance=instance)

    return render(request, 'leadsMasterApp/addGenPlan.html', {'form':form})


def IconicIntroducerView(request):
    today = datetime.now()
    minAge=100
    maxAge=0
    ageSum=0
    females=0
    males=0
    occupations={}


    introducers=Person.objects.filter(isintroducer=True)

    # Calculate number of leads and number of successful leads (leads that are current clients) given from each person
    numOfLeadsPerIntroducer ={}
    numOfSuccLeadsPerIntroducer={}
    for introducer in introducers:
        # Number of leads and number of successfull leads
        leadsFromThisIntroducer = Person.objects.filter(leadfrom=introducer)
        clientsFromThisIntroducer = Person.objects.filter(leadfrom=introducer, isclient=1)
        numOfLeadsPerIntroducer[introducer] = len(leadsFromThisIntroducer)
        numOfSuccLeadsPerIntroducer[introducer]= len(clientsFromThisIntroducer)

    #Calculate successful PERCENTAGE for each introducer
        # Where successful PERCENTAGE is ((successfulLeads/leads)*100
    #Create a list with introducers who have successful percentage over 70%
    successPercentage={}
    successfulIntroducers ={}
    for introducer in introducers:
        if numOfLeadsPerIntroducer[introducer]>0:
            percentage=numOfSuccLeadsPerIntroducer[introducer]/numOfLeadsPerIntroducer[introducer]*100.0
            successPercentage[introducer]= float("{0:.2f}".format(percentage))
        else:
            successPercentage[introducer]=0
        if successPercentage[introducer]>65:
            successfulIntroducers[introducer]=(successPercentage[introducer],numOfSuccLeadsPerIntroducer[introducer])

    # sucIntroPercenSorted has the successfull introducers sorted with the best first
    succIntroPercenSorted = OrderedDict(sorted(successfulIntroducers.items(), key=lambda v: v[1], reverse=True))

    #Calculate profit gained from each lead given from each introducer
    profits={}
    profithours={}
    for introducer in introducers:
        profits[introducer]=0
    for introducer in introducers:
        clientsFromThisIntroducer = Person.objects.filter(isclient='1', leadfrom=introducer)
        hours = 0
        for person in clientsFromThisIntroducer:
            # General Business profits from this introducer
            genContracts= GeneralContract.objects.filter(client = person,cancelled=False)
            if genContracts:
                for contract in genContracts:
                    profit = generalContractProfit(contract)
                    profits[introducer] += (profit * contract.years)

            # Life Business profits from this introducer
            lifeContr = LifeContract.objects.filter(client = person,cancelled=False)

            if lifeContr:
                LifeProfits={}
                for contract2 in lifeContr:
                    LifeProfits[contract2] = lifeContractProfit(contract2, contract2.client)
                    profit=LifeProfits[contract2]['total']
                    # sum up profit from this contract
                    profits[introducer] += profit
            # Get hours spent on person
            activities = Calendar.objects.filter(activity__customerid=person)
            for a in activities:
                hours += a.activity.duration
        profithours[introducer]=hours

    profitBased={}
    for key in profits:
        if profits[key]!=0:
            profitBased[key]=profits[key]
    profitBasedSorted = OrderedDict(sorted(profitBased.items(),key=lambda x:x[1], reverse=True))

    successProfitHours={}
    profitHoursDic={}
    successProfitHoursSorted={}
    for person in succIntroPercenSorted:
        successProfitHours[person] = {'percentage': succIntroPercenSorted[person], 'hours': float("{0:.2f}".format(profithours[person]/60))}
    successProfitHoursSorted = OrderedDict(sorted(successProfitHours.items(), key=lambda x: (-x[1]['percentage'][0],x[1]['hours'])))

    #Take first 20 people from successful Introducers
    finalProfitHours = {}
    if len(successProfitHoursSorted) > 20:
        for key in sorted(successProfitHoursSorted)[:20]:
            finalProfitHours[key] = successProfitHoursSorted[key]
    else:
        for key in sorted(successProfitHoursSorted):
            finalProfitHours[key] = successProfitHoursSorted[key]
    finalDicSorted = OrderedDict(sorted(finalProfitHours.items(), key=lambda x: (-x[1]['percentage'][0],x[1]['hours'])))

    for person in  finalDicSorted:
        personAge= relativedelta(today.date(), person.dateofbirth).years
        if personAge>maxAge:
            maxAge=personAge
        if personAge<minAge:
            minAge=personAge
        ageSum+=personAge
        if person.gender=="Female":
            females+=1
        else:
            males+=1
        if person.occupation not in occupations:
            occupations[person.occupation]=1
        else:
            occupations[person.occupation]+=1

    #Take introducers based on profit gained from leads
    for person in profitBasedSorted:
        profitHoursDic[person] = {'profit': profitBasedSorted[person], 'hours': float("{0:.2f}".format(profithours[person]/60))}
    profitHoursSortedIntro = OrderedDict(sorted(profitHoursDic.items(), key=lambda x: (-x[1]['profit'],x[1]['hours'])))

    #Take first 20 people from Introducers based on profit
    finalProfitBased = {}
    if len(profitHoursSortedIntro) > 20:
        for key in sorted(profitHoursSortedIntro)[:20]:
            finalProfitBased[key] = profitHoursSortedIntro[key]
    else:
        for key in sorted(profitHoursSortedIntro):
            finalProfitBased[key] = profitHoursSortedIntro[key]
    finalProfitBasedDicSorted = OrderedDict(sorted(finalProfitBased.items(), key=lambda x: (-x[1]['profit'],x[1]['hours'])))

    for person in finalProfitBasedDicSorted:
        personAge= relativedelta(today.date(), person.dateofbirth).years
        if personAge>maxAge:
            maxAge=personAge
        if personAge<minAge:
            minAge=personAge
        ageSum+=personAge
        if person.gender=="Female":
            females+=1
        else:
            males+=1
        if person.occupation not in occupations:
            occupations[person.occupation]=1
        else:
            occupations[person.occupation]+=1

    averageAge=ageSum/(len(finalDicSorted)+len(finalProfitBasedDicSorted))
    averageAge=float("{0:.2f}".format(averageAge))
    occupBasedSorted = OrderedDict(sorted(occupations.items(),key=lambda x:x[1], reverse=True))
    if len(occupBasedSorted)>4:
        occupBasedFinal = [k for k in sorted(occupBasedSorted.keys())[:4]]
    else:
        occupBasedFinal = [k for k in sorted(occupBasedSorted.keys())]

    genderAverage=""
    if males>females:
        genderAverage="Male"
    elif females>males:
        genderAverage="Female"
    else:
        genderAverage="Male/Female"

    return render(request, 'leadsMasterApp/iconicIntroducer.html', {'genderAverage':genderAverage,'minAge':minAge,'maxAge':maxAge,
                                                                    'averageAge':averageAge, 'finalDicSorted':finalDicSorted,
                                                                    'introducers':introducers, 'finalProfitBasedDicSorted': finalProfitBasedDicSorted,
                                                                    'occupBasedFinal':occupBasedFinal})


def IconicClientView(request):
    today = datetime.now()

    lifePlan = ""
    generalPlan=""
    if request.method == "POST":
        plansForm = PlansOptionsForm(data=request.POST)
        if plansForm.is_valid():
            generalPlan = plansForm.cleaned_data['generalPlan']
            lifePlan = plansForm.cleaned_data['lifePlan']
    else:
        plansForm=PlansOptionsForm()

    if (lifePlan!="") or (generalPlan!=""):
        clients= Person.objects.filter(isclient=1)
        # Calculate profit gained from each lead given from each introducer
        profits = {}
        for client in clients:
            if (not lifePlan) and generalPlan:
                # General Business profits from this client
                genContracts = GeneralContract.objects.filter(client=client, cancelled=False, plan=generalPlan.planid)
                if genContracts:
                    if client not in profits:
                        profits[client]=0
                    for contract in genContracts:
                        profit = generalContractProfit(contract)
                        profits[client] += (profit * (contract.years/12))
            elif (not generalPlan) and lifePlan:
                # Life Business profits from this introducer
                lifeContr = LifeContract.objects.filter(client=client, cancelled=False, plan=lifePlan.planlifeid)
                if lifeContr:
                    if client not in profits:
                        profits[client]=0
                    LifeProfits = {}
                    for contract2 in lifeContr:
                        LifeProfits[contract2] = lifeContractProfit(contract2, contract2.client)
                        profit = LifeProfits[contract2]['total']
                        # sum up profit from this contract
                        profits[client] += profit

        profitSorted = OrderedDict(sorted(profits.items(), key=lambda x: x[1], reverse=True))
    else:
        clients = Person.objects.filter(isclient=1)
        # Calculate profit gained from each lead given from each introducer
        profits = {}
        for client in clients:
            profits[client] = 0
        for client in clients:
            # General Business profits from this client
            genContracts = GeneralContract.objects.filter(client=client, cancelled=False)
            if genContracts:
                for contract in genContracts:
                    profit = generalContractProfit(contract)
                    profits[client] += (profit * (contract.years/12))

            # Life Business profits from this introducer
            lifeContr = LifeContract.objects.filter(client=client, cancelled=False)

            if lifeContr:
                LifeProfits = {}
                for contract2 in lifeContr:
                    LifeProfits[contract2] = lifeContractProfit(contract2, contract2.client)
                    profit = LifeProfits[contract2]['total']
                    # sum up profit from this contract
                    profits[client] += profit

        profitSorted = OrderedDict(sorted(profits.items(), key=lambda x: x[1], reverse=True))

    minAge = 100
    maxAge = 0
    ageSum = 0
    females = 0
    males = 0
    occupations = {}
    averageAge=0
    genderAverage = ""
    occupBasedFinal="-"
    profitHours = {}
    profitHoursSorted={}
    if profitSorted:
        for person in profitSorted:
            #Get hours spent on person
            hours = 0
            activities=Calendar.objects.filter(activity__customerid=person)
            for a in activities:
                hours+= a.activity.duration
            profitHours[person] = {'profit': float("{0:.2f}".format(profitSorted[person])), 'hours': float("{0:.2f}".format(hours/60))}

        profitHoursSorted = OrderedDict(sorted(profitHours.items(), key=lambda x: (-x[1]['profit'],x[1]['hours'])))
        finalDic={}
        if len(profitHoursSorted)>20:
            for key in sorted(profitHoursSorted)[:20]:
                finalDic[key]= profitHoursSorted[key]
        else:
            for key in sorted(profitHoursSorted):
                finalDic[key]= profitHoursSorted[key]
        finalDicSorted= OrderedDict(sorted(finalDic.items(), key=lambda x: (-x[1]['profit'],x[1]['hours'])))

    if finalDicSorted:
        for person in finalDicSorted:
            # Get age and Gender
            personAge = relativedelta(today.date(), person.dateofbirth).years
            if personAge > maxAge:
                maxAge = personAge
            if personAge < minAge:
                minAge = personAge
            ageSum += personAge
            if person.gender == "Female":
                females += 1
            else:
                males += 1

            # Get occupation of people
            if person.occupation not in occupations:
                occupations[person.occupation] = 1
            else:
                occupations[person.occupation] += 1

    averageAge = ageSum / (len(finalDicSorted))
    print averageAge
    averageAge = float("{0:.2f}".format(averageAge))
    occupBasedSorted = OrderedDict(sorted(occupations.items(), key=lambda x: x[1], reverse=True))
    if len(occupBasedSorted) > 4:
        occupBasedFinal = [k for k in sorted(occupBasedSorted.keys())[:4]]
    else:
        occupBasedFinal = [k for k in sorted(occupBasedSorted.keys())]

    if males > females:
        genderAverage = "Male"
    elif females > males:
        genderAverage = "Female"
    else:
        genderAverage = "Male/Female"
    return render(request, 'leadsMasterApp/iconicClient.html',{'genderAverage':genderAverage,'minAge':minAge,'maxAge':maxAge,
                                                                    'averageAge':averageAge, 'clients':clients,
                                                                     'finalDicSorted': finalDicSorted,
                                                                    'occupBasedFinal':occupBasedFinal,
                                                               'plansForm':plansForm})

def paymentsReportView(request):
    today = datetime.now()

    toBePaidGeneral={}
    toBePaidLife = {}
    upcomingGeneral ={}
    upcomingLife = {}
    for item in GeneralContract.objects.filter(nextpayment__lte=today.date(), cancelled=False):
        contract=item
        nextPayment = float("{0:.2f}".format(contract.price / int(contract.doses)))
        toBePaidGeneral[contract]=nextPayment
    for item in LifeContract.objects.filter(nextpayment__lte=today.date(), cancelled=False):
        contract=item
        nextPayment = float("{0:.2f}".format(contract.price / int(contract.doses)))
        toBePaidLife[contract]=nextPayment
    for item in GeneralContract.objects.filter(nextpayment__range=[(today.date() + timedelta(days=1)),(today.date() + timedelta(days=6))] , cancelled=False):
        contract=item
        nextPayment = float("{0:.2f}".format(contract.price / int(contract.doses)))
        upcomingGeneral[contract]=nextPayment
    for item in LifeContract.objects.filter(nextpayment__range=[(today.date() + timedelta(days=1)),(today.date() + timedelta(days=6))], cancelled=False):
        contract = item
        nextPayment = float("{0:.2f}".format(contract.price / int(contract.doses)))
        upcomingLife[contract] = nextPayment
    return render(request, 'leadsMasterApp/paymentsPage.html', {'toBePaidLife':toBePaidLife,
                                                                'toBePaidGeneral':toBePaidGeneral,
                                                                'upcomingGeneral':upcomingGeneral,
                                                                'upcomingLife':upcomingLife})
