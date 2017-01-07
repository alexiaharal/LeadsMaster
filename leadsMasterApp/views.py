from __future__ import division

from calendar import monthrange

from django.shortcuts import render, get_object_or_404,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect, Http404
from reportlab.pdfgen import canvas
from django.template.context import RequestContext
from datetime import datetime, timedelta, date
from .models import Calendar, Person, Activity, GeneralContract, LifeContract,Company, Generalbusinessplans, \
    Lifebusinessplans
from django.db.models import Q
from .forms import SearchForm, PersonForm, LifeContractForm, CompanyForm,GeneralPlansForm,LifePlansForm, GeneralContractForm, UserForm, UserProfileForm, \
    ActivityForm, CalendarForm
from collections import OrderedDict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

def IndexView(request):
    #Gather all activities for current day
    activities=[]
    for a in Activity.objects.filter(date=today.date()):
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
    for a in Activity.objects.filter(date=today.date()):
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
    for contract in GeneralContract.objects.filter(expirationdate__date=today.date(), cancelled=False):
        generalrenewals.append(contract)
    liferenewals = []
    for contract in LifeContract.objects.filter(expirationdate__date=today.date(),cancelled=False):
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


def calendar(request,day=None,month=None,year=None):
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

    return render(request,'leadsMasterApp/calendar.html',{'calendarEntries':calendarEntries,'dailyEntries':dailyEntries,'form1':form1,'form2': form2})


def successfulLeadsPercentage(introducer):
    numOfLeads = 0
    numOfSuccLeads = 0
    leadsFromIntroducer = Person.objects.filter(leadfrom=introducer.idperson)
    # Calculate
    for person in leadsFromIntroducer:
        numOfLeads += 1
        if person.isclient == 1:
            numOfSuccLeads += 1
    #Calculate successful PERCENTAGE
        # Where successful PERCENTAGE is ((leads-successfulLeads)/leads)*100
    successfulPercentage=0
    successfulIntroducers ={}
    if numOfLeads>0:
        percentage=numOfSuccLeads/numOfLeads*100.0
    else:
        percentage=0
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
    activities= Calendar.objects.filter(activity__customerid=person)
    totalHours=0
    for a in activities:
        totalHours+= a.activity.duration
    totalHours=totalHours/60
    totalHours=float("{0:.2f}".format(totalHours))
    return render(request, 'leadsMasterApp/manHoursPerson.html', {'person':person,'activities':activities,'totalHours':totalHours})

def AddProfileView(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.save()
            return redirect('ourPeople')
    else:
        form=PersonForm()
    return render(request, 'leadsMasterApp/addProfile.html', {'form':form})

def EditProfileView(request, pk):
    person = get_object_or_404(Person, pk=pk)
    form = PersonForm(data = request.POST or None, instance=person)
    if form.is_valid():
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
    print instance
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

    return render(request, 'leadsMasterApp/addGenPlan.html', {'form':form})

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
                            percentage = plan.maxpercentage
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


