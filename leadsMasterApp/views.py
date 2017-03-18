from __future__ import print_function
from __future__ import division

from calendar import monthrange

from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import RequestContext
from datetime import datetime, timedelta, date, time

from django.conf import settings
from .models import Calendar, Person, Activity, GeneralContract, LifeContract, Company, Generalbusinessplans, \
    Lifebusinessplans, birthdayNot, genRenewalsNot, lifeRenewalsNot, genPaymentsNot, lifePaymentsNot, UserProfile
from django.db.models import Q
from django.core.mail import send_mail

from .forms import SearchForm, PersonForm, LifeContractForm, CompanyForm, GeneralPlansForm, LifePlansForm, \
    GeneralContractForm, UserForm, UserProfileForm, \
    ActivityForm, CalendarForm, DatesForm, PlansOptionsForm, renewalPeriodForm
from collections import OrderedDict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta

#####----- Views -----######

today = datetime.now()


# Register An admin user only when one is not already created
def registerAdmin(request):
    # get the request's context.
    context = RequestContext(request)
    registered = False
    # Check whether an admin is already registered
    admins = User.objects.filter(is_superuser=True, is_staff=True)
    if admins.count()>0:
        allowed = False
    else:
        allowed = True

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        # If form is valid
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            # tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else
        else:
            print(user_form.errors)

    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request,
                  'leadsMasterApp/registerAdmin.html',
                  {'user_form': user_form, 'registered': registered, 'allowed': allowed},
                  context)


# Register a user/employee of the system
def register(request):
    # get the request's context.
    context = RequestContext(request)

    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're processing form data.
    if request.method == 'POST':
        # Combine user form and profile form
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

            # tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        else:
            print (user_form.errors, profile_form.errors)

    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'leadsMasterApp/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
                  context)


# Login Form view
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
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'leadsMasterApp/login.html', {}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect('login')

actEmails = {}


# Index or Home Page Handler View
def IndexView(request):
    if request.user.is_authenticated():
        today = datetime.now()

        # Gather all activities for current day
        activities = []
        for a in Activity.objects.filter(date=today.date()):
            activities.append(a)

            # Notification Component
            if a.customerid.email:
                # Check if an email was already sent
                if a.email == False:
                    # insert code here to send email if wanted
                    a.email = True
                    a.save()

        # Gather birthdays for current day
        birthdays = []
        emails = []
        for p in Person.objects.filter(dateofbirth__month=today.month, dateofbirth__day=today.day):
            birthdays.append(p)
            birthdayTable = birthdayNot.objects.all()

            # Notification Component - check if an email was already sent
            # I.e. check if a unique entry is already in the corresponding table
            if birthdayTable.filter(birthday=p, date=today.date()).exists():
                flag = True
            else:
                if p.email:
                    emails.append(p.email)
                    obj = birthdayNot(birthday=p, date=today.date(), email=True)
                    obj.save()
        # If there are emails to be sent, send them
        if emails:
            send_mail(
                'Happy Birthday',
                'Leads Master system, on behalf of your insurance agent, wishes you a very happy birthday.',
                settings.EMAIL_HOST_USER,
                emails
            )

        # Gather  General renewals for current day
        generalrenewals = []
        for contract in GeneralContract.objects.filter(expirationdate=today.date(), cancelled=False):
            generalrenewals.append(contract)

            # Notification Component - check if an email was already sent
            # I.e. check if a unique entry is already in the corresponding table
            genRenTable = genRenewalsNot.objects.all()
            if genRenTable.filter(renewal=contract, date=today.date()).exists():
                flag = True
            else:
                if contract.client.email:
                    plans = ""
                    for p in contract.plan.all():
                        plans += str(p)
                    text = 'This is a reminder that your ' + plans + ' contract, with contract number: ' + str(
                        contract.idcontract) + ' is expiring today! Please get in touch to renew. Thank you, Leads Master'
                    send_mail(
                        'Contract Renewal Reminder',
                        text,
                        settings.EMAIL_HOST_USER,
                        [contract.client.email]
                    )
                    obj = genRenewalsNot(renewal=contract, date=today.date(), email=True)
                    obj.save()

        # Gather Life renewals for current day
        liferenewals = []
        for contract in LifeContract.objects.filter(expirationdate=today.date(), cancelled=False):
            liferenewals.append(contract)

            # Notification Component - check if an email was already sent
            # I.e. check if a unique entry is already in the corresponding table
            lifeRenTable = lifeRenewalsNot.objects.all()
            if lifeRenTable.filter(renewal=contract, date=today.date()).exists():
                flag = True
            else:
                if contract.client.email:
                    plans = ""
                    for p in contract.plan.all():
                        plans += str(p)
                    text = 'This is a reminder that your ' + plans + ' contract, with contract number: ' + str(
                        contract.idcontract) + ' is expiring today! If you dont\' want it to be renewed please get in touch. Thank you, Leads Master'
                    send_mail(
                        'Contract Renewal Notification',
                        text,
                        settings.EMAIL_HOST_USER,
                        [contract.client.email]
                    )
                    obj = lifeRenewalsNot(renewal=contract, date=today.date(), email=True)
                    obj.save()

        # Gather General payments for current day
        generalpayments = []
        for contract in GeneralContract.objects.filter(nextpayment=today.date(), cancelled=False):
            generalpayments.append(contract)

            # Notification Component - check if an email was already sent
            # I.e. check if a unique entry is already in the corresponding table
            genPaymTable = genPaymentsNot.objects.all()
            if genPaymTable.filter(payment=contract, date=today.date()).exists():
                flag = True
            else:
                if contract.client.email:
                    plans = ""
                    for p in contract.plan.all():
                        plans += str(p)
                    text = 'This is a reminder that your ' + plans + ' contract, with contract number: ' + str(
                        contract.idcontract) \
                           + ' needs to be paid! Please get in touch to arrange a meeting. Thank you, Leads Master'

                    send_mail(
                        'Contract Payment Reminder',
                        text,
                        settings.EMAIL_HOST_USER,
                        [contract.client.email]
                    )
                    obj = genPaymentsNot(payment=contract, date=today.date(), email=True)
                    obj.save()

        # Gather Life payments for current day
        lifepayments = []
        for contract in LifeContract.objects.filter(nextpayment=today.date(), cancelled=False):
            lifepayments.append(contract)

            # Notification Component - check if an email was already sent
            # I.e. check if a unique entry is already in the corresponding table
            lifePaymTable = lifePaymentsNot.objects.all()
            if lifePaymTable.filter(payment=contract, date=today.date()).exists():
                flag = True
            else:
                if contract.client.email:
                    plans = ""
                    for p in contract.plan.all():
                        plans += str(p)
                    text = 'This is a reminder that your ' + plans + ' contract, with contract number: ' + str(
                        contract.idcontract) + ' needs to be paid! Please get in touch to arrange a meeting. Thank you, Leads Master'
                    send_mail(
                        'Contract Payment Reminder',
                        text,
                        settings.EMAIL_HOST_USER,
                        [contract.client.email]
                    )
                    obj = lifePaymentsNot(payment=contract, date=today.date(), email=True)
                    obj.save()

        # Automatically renew Life contracts
        yesterday = today - timedelta(1)
        for contract in LifeContract.objects.filter(expirationdate__lt=today.date(), cancelled=False):
            c = contract
            newDate = c.expirationdate + relativedelta(years=+1)
            c.expirationdate = newDate
            c.save()

        # Choose 10 random records to show
        if today.weekday() == 0:
            result_entities = []
            for p in Person.objects.raw('SELECT * FROM leadsMasterApp_Person WHERE isclient=0 ORDER BY RANDOM() LIMIT 10'):
                result_entities.append(p)
        else:
            result_entities = []

        # Gather sales this day last year
        Generalsales = []
        Lifesales = []
        totalGeneralSales = 0
        totalLifeSales = 0
        # Sum Up Sales Past Years This Day
        for contract in GeneralContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
            Generalsales.append(contract)
            totalGeneralSales += contract.annualpremium

        for contract in LifeContract.objects.filter(issuedate__day=today.day, issuedate__month=today.month):
            Lifesales.append(contract)
            totalLifeSales += contract.annualpremium

        return render(request, 'leadsMasterApp/indexBase.html',
                      {'generalrenewals': generalrenewals, 'generalpayments': generalpayments,
                       'activities': activities, 'birthdays': birthdays, 'lifesales': Lifesales,
                       'generalsales': Generalsales, 'totalGeneralSales': totalGeneralSales,
                       'liferenewals': liferenewals, 'lifepayments': lifepayments,
                       'totalLifeSales': totalLifeSales,
                       'result_entities': result_entities})
    else:
        return redirect('login')


# Calendar Page Handler View
def calendar(request, day=None, month=None, year=None):
    today = datetime.now()
    calendar_entries = Calendar.objects.all()
    if day is None:
        day = today.date().day
        month = today.date().month
        year = today.date().year
    # Gather current days entries
    daily_entries = Calendar.objects.filter(activity__date__day=day, activity__date__month=month, activity__date__year=year)

    # Handle Insert Calendar Entry Form
    if request.method == "POST":
        # Combine both forms
        form1 = ActivityForm(request.POST)
        form2 = CalendarForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            activity = form1.save(commit=False)
            activity.save()
            calendar = form2.save(commit=False)
            employee = form2.cleaned_data['employee']
            calendar_entry = Calendar(activity=activity, employee=employee)
            calendar_entry.save()
            return redirect('calendar')
    else:
        form1 = ActivityForm()
        form2 = CalendarForm()
    return render(request, 'leadsMasterApp/calendar.html',
                  {'day': day, 'month': month, 'year': year,
                   'daily_entries': daily_entries, 'form1': form1, 'form2': form2})


# Edit Calendar Entry Handler View
def edit_Calendar_Entry(request, pkc):
    entryCalendar = get_object_or_404(Calendar,entryid=pkc)
    act = entryCalendar.activity.activityid
    entryActivity = get_object_or_404(Activity,activityid=act)
    formActivity = ActivityForm(data=request.POST or None, instance=entryActivity)
    formCalendar = CalendarForm(data=request.POST or None, instance=entryCalendar)
    if formActivity.is_valid() and formCalendar.is_valid():
        entryActivity = formActivity.save(commit=False)
        entryActivity.save()
        entryCalendar = formCalendar.save(commit=False)
        entryCalendar.save()
        return redirect('calendar')
    return render(request, 'leadsMasterApp/editCalendarEntry.html', {'formActivity':formActivity,'formCalendar': formCalendar})


# Our People Page Handler View
def OurPeopleView(request):
    # Check if search requested
    query = ""
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['searchbox']
    else:
        form = SearchForm()

    # Get corresponding results. Check name, surname or id.
    if query != "":
        people = []
        for p in Person.objects.filter(Q(name__startswith=query)):
            if p not in people:
                people.append(p)
        for p in Person.objects.filter(Q(surname__startswith=query)):
            if p not in people:
                people.append(p)
        for p in Person.objects.filter(Q(idperson__startswith=query)):
            if p not in people:
                people.append(p)
    else:
        people = []
        for p in Person.objects.raw('SELECT * FROM leadsMasterApp_Person '):
            people.append(p)

    return render(request, 'leadsMasterApp/ourPeople.html', {'form': form, 'people': people})


# Report: Man Hours View Report Handler View
def ManHoursView(request):
    # Check if search requested
    query = ""
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['searchbox']
    else:
        form = SearchForm()

    if query != "":
        people = []
        for p in Person.objects.filter(Q(name__startswith=query)):
            if p not in people:
                people.append(p)
        for p in Person.objects.filter(Q(surname__startswith=query)):
            if p not in people:
                people.append(p)
        for p in Person.objects.filter(Q(idperson__startswith=query)):
            if p not in people:
                people.append(p)
    else:
        people = []
        for p in Person.objects.raw('SELECT * FROM leadsMasterApp_Person'):
            people.append(p)

    return render(request, 'leadsMasterApp/manHoursBase.html', {'form': form, 'people': people})


# Detailed Man Hours of a particular person page handler view
def ManHoursPersonView(request, pk):
    person = get_object_or_404(Person, pk=pk)
    activities = Calendar.objects.filter(activity__customerid=person).order_by('activity__date')
    totalHours = 0
    for a in activities:
        totalHours += a.activity.duration
    totalHours = totalHours / 60
    totalHours = float("{0:.2f}".format(totalHours))
    return render(request, 'leadsMasterApp/manHoursPerson.html',
                  {'person': person, 'activities': activities, 'totalHours': totalHours})


# Report: Successful Introducers
def SuccLeadsView(request):
    query = ""
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['searchbox']
    else:
        form = SearchForm()

    if query != "":
        introducers = Person.objects.all()
        resultIntroducers = []
        myintroducers = {}
        flag = 1
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
            percentage = successfulLeadsPercentage(p)
            myintroducers[p] = percentage
    else:
        introducers = Person.objects.filter(isintroducer=1)
        topIntroducers = {}
        myintroducers = {}
        flag = 0
        for p in introducers:
            percentage = successfulLeadsPercentage(p)
            topIntroducers[p] = percentage
            myintroducers = OrderedDict(sorted(topIntroducers.items(), key=lambda x: x[1], reverse=True))

    return render(request, 'leadsMasterApp/succLeads.html',
                  {'form': form, 'flag': flag, 'myintroducers': myintroducers})


# Detailed view of leads given from a person view
def succLeadsPersonView(request, pk):
    person = get_object_or_404(Person, pk=pk)
    leads = Person.objects.filter(leadfrom=person)
    successfulLeads = leads.filter(isclient=1)
    numOfLeads = len(leads)
    numOfSuccLeads = len(successfulLeads)
    percentage = successfulLeadsPercentage(person)
    return render(request, 'leadsMasterApp/succLeadsPerson.html',
                  {'numOfLeads': numOfLeads, 'numOfSuccLeads': numOfSuccLeads, 'percentage': percentage,
                   'successfulLeads': successfulLeads, 'person': person, 'leads': leads})


# Report: Sales Report
def salesReportsView(request):
    today = datetime.now()

    date1 = ""
    date2 = ""
    lifePlan = ""
    generalPlan = ""
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

    ###### The difference here of sales and profits reports is that
    ###### dates for sales are the issue dates of the contract (including issue year)
    ###### dates for profits are the issue days and months to calculate what profits
    ###### the agent is going to gain within that month

    if (date1 == "") and (date2 == ""):
        currentGenSales = GeneralContract.objects.filter(issuedate__month=today.month, issuedate__year=today.year,
                                                         cancelled=False)
        currentLifeSales = LifeContract.objects.filter(issuedate__month=today.month, issuedate__year=today.year,
                                                       cancelled=False)
        currentGenProfits = GeneralContract.objects.filter(issuedate__month=today.month, cancelled=False)
        currentLifeProfits = LifeContract.objects.filter(issuedate__month=today.month, cancelled=False)
    else:
        #Get sales contracts between those dates
        currentGenSales = GeneralContract.objects.filter(issuedate__range=[date1, date2], cancelled=False)
        currentLifeSales = LifeContract.objects.filter(issuedate__range=[date1, date2], cancelled=False)
        #Get profit contracts between those dates
        currentGenProfits = GeneralContract.objects.filter(Q(issuedate__month = date1.month) | Q(issuedate__month = date2.month) ,cancelled=False)
        currentGenProfits = currentGenProfits.exclude(Q(issuedate__month = date1.month) & Q(issuedate__day__lte = date1.day))
        currentGenProfits = currentGenProfits.exclude(Q(issuedate__month = date2.month) & Q(issuedate__day__gte = date2.day))

        currentLifeProfits = LifeContract.objects.filter(Q(issuedate__month = date1.month) | Q(issuedate__month = date2.month) ,cancelled=False)
        currentLifeProfits = currentLifeProfits.exclude(Q(issuedate__month = date1.month) & Q(issuedate__day__lte = date1.day))
        currentLifeProfits = currentLifeProfits.exclude(Q(issuedate__month = date2.month) & Q(issuedate__day__gte = date2.day))


    if (lifePlan != "") or (generalPlan != ""):
        if (not lifePlan) and generalPlan:
            currentGenSales = currentGenSales.filter(plan=generalPlan.planid)
            currentLifeSales = {}
            currentGenProfits = currentGenProfits.filter(plan=generalPlan.planid)
            currentLifeProfits = {}
        elif (not generalPlan) and lifePlan:
            currentGenSales = {}
            currentLifeSales = currentLifeSales.filter(plan=lifePlan.planlifeid)
            currentGenProfits = {}
            currentLifeProfits = currentLifeProfits.filter(plan=lifePlan.planlifeid)


    #### Sales Calculations ######
    # Calculate total Annual Premium for General Sales
    totalCurrentAnnualGen = 0
    for sale in currentGenSales:
        totalCurrentAnnualGen += sale.annualpremium

    # Calculate total Annual Premium for General Sales
    totalCurrentAnnualLife = 0
    for sale in currentLifeSales:
        totalCurrentAnnualLife += sale.annualpremium

    # Calculate profits and total profit for General Sales Report
    generalSalesProfits = {}
    totalGeneralSalesProfit = 0
    for contract in currentGenSales:
        generalSalesProfits[contract] = generalContractProfit(contract)
        totalGeneralSalesProfit += generalSalesProfits[contract]

    # Calculate profits and total profit for General Profits Report
    generalProfits = {}
    totalGeneralProfit = 0
    for contract in currentGenProfits:
        generalProfits[contract] = generalContractProfit(contract)
        totalGeneralProfit += generalProfits[contract]

    # Calculate profits and total profit for Life Sales Report
    totalLifeSalesProfits = {}
    totalLifeSalesProfit = 0
    for contract in currentLifeSales:
        totalLifeSalesProfits[contract] = lifeContractProfit(contract, contract.client)
        totalLifeSalesProfit += totalLifeSalesProfits[contract]["thisYearProfit"]

    # Calculate profits and total profit for Life Profits Report
    totalLifeProfits = {}
    totalLifeProfit = 0
    for contract in currentLifeProfits:
        totalLifeProfits[contract] = lifeContractProfit(contract, contract.client)
        totalLifeProfit += totalLifeProfits[contract]["thisYearProfit"]

    ###### Profits Calculations #####
    return render(request, 'leadsMasterApp/salesReports.html', {'totalLifeSalesProfits': totalLifeSalesProfits,
                                                                'totalLifeSalesProfit': totalLifeSalesProfit,
                                                                'totalCurrentAnnualLife': totalCurrentAnnualLife,
                                                                'form': form,
                                                                'generalSalesProfits': generalSalesProfits,
                                                                'totalGeneralSalesProfit': totalGeneralSalesProfit,
                                                                'totalCurrentAnnualGen': totalCurrentAnnualGen,
                                                                'totalLifeProfits': totalLifeProfits,
                                                                'totalLifeProfit': totalLifeProfit,
                                                                'generalProfits': generalProfits,
                                                                'totalGeneralProfit': totalGeneralProfit,
                                                                'plansForm': plansForm
                                                                })

# This function calculates the profit gained from
# a given contract any year, since the profit for
# general contracts is every year the same amount.


def generalContractProfit(contract):
    profitPercentage = 0
    for plan in contract.plan.all():
        profitPercentage += plan.commission
    print (contract.basicvalue)
    profit = (contract.basicvalue * profitPercentage / 100)
    print (profit)
    return profit

# This function calculates the profit gained from a
# given life contract. It returns a dictionary of the form
# {'total': amount A , 'thisYearProfit': amount B }, which
# contains the total profit gained from this contract during all
# years of issue , and the profit gained current year.

def lifeContractProfit(contract, person):
    today = datetime.now()
    yearsOfContract = relativedelta(today.date(), contract.issuedate).years
    first_year = 0
    nextyears = 0
    # get profit from all plans if more than one plan
    for plan in contract.plan.all():
        # Calculate FIRST year's profit
        # Get profit percentage of first year

        # If this contract is of type Life Plan C which contains more than one future profits
        # and makes the percentage being just the first year commission percentage
        if plan.futureprofit2 or plan.futureprofit3 or plan.futureprofit4:
            percentage = plan.firstyearcommission
        # If contract has duration, then is of type Life Plan B
        # which makes the percentage being the duration multiplied by the first year commission
        elif contract.duration:
            percentage = contract.duration * plan.firstyearcommission
        # Else if it is of type Life  Plan A then the percentage is
        # the years difference of the age limit and the person's years
        # multiplied by the first year commission
        else:
            percentage = (plan.agelimit - (
                relativedelta(today.date(), person.dateofbirth).years)) * plan.firstyearcommission

        # Check if in range of percentages
        if percentage < plan.minpercentage:
            percentage = plan.minpercentage
        elif percentage > plan.maxpercentage:
            percentage = plan.maxpercentage
        # Save final First Year's Commission Percentage
        first_year = percentage
#######################
        # REST OF THE YEARS profit calculation - up to now
        # If current contract is issued for more than one year
        if yearsOfContract > 0:
            # If type: Life Plan C
            if plan.futureprofit2 or plan.futureprofit3 or plan.futureprofit4:
                # If this is the second year of issue, get percentage of profit
                if yearsOfContract == 1:
                    nextyears += plan.futureprofit2
                    thisYearProfit = plan.futureprofit2
                # If this is the third year of issue
                elif yearsOfContract == 2:
                    nextyears += plan.futureprofit3 + plan.futureprofit2
                    thisYearProfit = plan.futureprofit3
                # For next years of issue
                else:
                    nextyears += ((plan.futureprofit3 + plan.futureprofit2 + plan.futureprofit4) * (yearsOfContract - 2))
                    thisYearProfit = plan.futureprofit4
            # Else if of type Life Plan A or Life Plan B
            else:
                nextyears += plan.futureprofit
                thisYearProfit = plan.futureprofit
        # If this is the first year of issue
        else:
            thisYearProfit = first_year

    # sum up profits from this contract
    totalProfit = (first_year * contract.basicvalue / 100) + (nextyears * yearsOfContract * contract.basicvalue / 100)
    profit = {}
    totalProfit = float("{0:.2f}".format(totalProfit))
    thisYearProfit = float("{0:.2f}".format(thisYearProfit))
    profit['total'] = totalProfit
    profit['thisYearProfit'] = thisYearProfit * contract.basicvalue / 100
    return profit


# Add a profile, i.e. Person entity
def AddProfileView(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            if form.cleaned_data['leadfrom']:
                introducer = Person.objects.get(idperson=form.cleaned_data['leadfrom'].idperson)
                if introducer.isintroducer == 0:
                    introducer.isintroducer = 1
                    introducer.save()
            person.save()
            return redirect('ourPeople')
    else:
        form = PersonForm()
    return render(request, 'leadsMasterApp/addProfile.html', {'form': form})


# Edit a profile, i.e. Person entity
def EditProfileView(request, pk):
    person = get_object_or_404(Person, pk=pk)
    form = PersonForm(data=request.POST or None, instance=person)
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


# Profile Page
def ProfileView(request, pk):
    person = get_object_or_404(Person, pk=pk)
    generalContracts = GeneralContract.objects.filter(client=person, cancelled=False)
    lifeContracts = LifeContract.objects.filter(client=person, cancelled=False)
    leads = Person.objects.filter(leadfrom=person)
    percentage = successfulLeadsPercentage(person)
    return render(request, 'leadsMasterApp/profile.html',
                  {'person': person, 'generalContracts': generalContracts,
                   'lifeContracts': lifeContracts, 'leads': leads, 'percentage': percentage})


# Contract Page
def ContractPageView(request, pk, type):
    today = datetime.now()

    # Check if is a life or general contract
    if type == 'life':
        contract = get_object_or_404(LifeContract, pk=pk)
        life = 1
        t = 'life'
        yearsInyears = ""
    else:
        contract = get_object_or_404(GeneralContract, pk=pk)
        life = 0
        t = 'general'
        yearsInyears = contract.years / 12
        if yearsInyears < 1:
            yearsInyears = 0
        yearsInyears = float("{0:.2f}".format(yearsInyears))

    person = contract.client
    # Calculate current dose amount
    totalPayment = contract.annualpremium
    if contract.nextpayment != "":
        nextPayment = float("{0:.2f}".format(contract.annualpremium / contract.doses))
    else:
        nextPayment = ""

    # Check if this contract has expired
    expired = 0
    if contract.expirationdate < today.date():
        expired = 1
    # Renewal form handler
    if request.method == "POST":
        form = renewalPeriodForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['other'] == "":
                period = form.cleaned_data['period']
            else:
                period = form.cleaned_data['other']
            c = contract
            newExpDate = c.expirationdate + relativedelta(months=+int(period))
            if (t=='general'):
                c.years += int(period)
            c.issuedate = c.expirationdate
            c.expirationdate = newExpDate
            c.save()
            return redirect('contractPage', pk=pk, type=t)
    else:
        form = renewalPeriodForm()

    return render(request, 'leadsMasterApp/contractPage.html',
                  {'contract': contract, 'life': life,
                   'person': person, 'totalPayment': totalPayment, 'yearsInyears': yearsInyears,
                   'nextPayment': nextPayment, 'expired': expired, 'form': form})


# Add a Life Contract entity
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
            print(contract_form.errors)
    else:
        contract_form = LifeContractForm()
    return render(request,
                  'leadsMasterApp/addContractLife.html',
                  {'add_contract_form': contract_form})


# Edit a Life Contract entity
def editContractLifeView(request, pk):
    instance = get_object_or_404(LifeContract, pk=pk)
    form = LifeContractForm(data=request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        p = Person.objects.get(idperson=form.cleaned_data['client'].idperson)
        if p.isclient == 0:
            p.isclient = 1
            p.save()
        if form.cleaned_data['cancelled'] == True:
            p.wasclient = 1
            contractsOfPersonLife = LifeContract.objects.filter(client=p, cancelled=False)
            contractsOfPersonGeneral = GeneralContract.objects.filter(client=p, cancelled=False)
            if len(contractsOfPersonGeneral) == 0 and len(contractsOfPersonLife) == 1:
                p.isclient = 0
            p.save()
        instance.save()
        form.save_m2m()
        return redirect('ProfileView', pk=p.id)

    return render(request,
                  'leadsMasterApp/addContractLife.html',
                  {'add_contract_form': form})


# Add a General Contract entity
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
            print (contract_form.errors)
    else:
        contract_form = GeneralContractForm()
    return render(request,
                  'leadsMasterApp/addContractGeneral.html',
                  {'add_contract_form': contract_form})


# Edit a General Contract entity
def editContractGeneralView(request, pk):
    instance = get_object_or_404(GeneralContract, pk=pk)
    form = GeneralContractForm(data=request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        p = Person.objects.get(idperson=form.cleaned_data['client'].idperson)
        if p.isclient == 0:
            p.isclient = 1
            p.save()
        if form.cleaned_data['cancelled'] == True:
            p.wasclient = 1
            contractsOfPersonLife = LifeContract.objects.filter(client=p, cancelled=False)
            contractsOfPersonGeneral = GeneralContract.objects.filter(client=p, cancelled=False)
            if len(contractsOfPersonGeneral) == 1 and len(contractsOfPersonLife) == 0:
                p.isclient = 0
            p.save()
        instance.save()
        form.save_m2m()
        return redirect('ProfileView', pk=p.id)

    return render(request,
                  'leadsMasterApp/addContractGeneral.html',
                  {'add_contract_form': form})


# Reports page handler view
def ReportsView(request):
    table = Person.objects.all()
    return render(request, 'leadsMasterApp/reports.html', {'table': table})


# Companies page handler View
def CompaniesView(request):
    companies = Company.objects.all()
    genPlans = Generalbusinessplans.objects.filter(deleted=False).order_by('company')
    lifePlans = Lifebusinessplans.objects.filter(deleted=False).order_by('company')

    return render(request, 'leadsMasterApp/companies.html',
                  {'companies': companies, 'genPlans': genPlans, 'lifePlans': lifePlans})


# Add Company entity
def AddCompanyView(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            return redirect('companies')
    else:
        form = CompanyForm()

    return render(request, 'leadsMasterApp/addCompany.html', {'form': form})


# Edit Company entity
def EditCompanyView(request, pk):
    instance = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=instance)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            return redirect('companies')
    else:
        form = CompanyForm(instance=instance)

    return render(request, 'leadsMasterApp/addCompany.html', {'form': form})


# Add General Plan entity
def AddGenPlanView(request):
    if request.method == "POST":
        form = GeneralPlansForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('companies')
    else:
        form = GeneralPlansForm()

    return render(request, 'leadsMasterApp/addGenPlan.html', {'form': form})


# Edit General Plan entity
def EditGenPlanView(request, pk):
    instance = get_object_or_404(Generalbusinessplans, pk=pk)
    if request.method == "POST":
        form = GeneralPlansForm(request.POST, instance=instance)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('companies')
    else:
        form = GeneralPlansForm(instance=instance)

    return render(request, 'leadsMasterApp/addGenPlan.html', {'form': form})


# Add Life Plan entity
def AddLifePlanView(request):
    if request.method == "POST":
        form = LifePlansForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('companies')
    else:
        form = LifePlansForm()

    return render(request, 'leadsMasterApp/addLifePlan.html', {'form': form})


# Edit Life Plan entity
def EditLifePlanView(request, pk):
    instance = get_object_or_404(Lifebusinessplans, pk=pk)
    if request.method == "POST":
        form = LifePlansForm(request.POST, instance=instance)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('companies')
    else:
        form = LifePlansForm(instance=instance)

    return render(request, 'leadsMasterApp/addGenPlan.html', {'form': form})


# Report: Iconic Introducer Profile
def IconicIntroducerView(request):
    today = datetime.now()
    minAge = 100
    maxAge = 0
    ageSum = 0
    females = 0
    males = 0
    occupations = {}

    introducers = Person.objects.filter(isintroducer=True)

    # Calculate number of leads and number of successful leads (leads that are current clients) given from each person
    numOfLeadsPerIntroducer = {}
    numOfSuccLeadsPerIntroducer = {}
    for introducer in introducers:
        # Number of leads and number of successfull leads
        leadsFromThisIntroducer = Person.objects.filter(leadfrom=introducer)
        clientsFromThisIntroducer = Person.objects.filter(leadfrom=introducer, isclient=1)
        numOfLeadsPerIntroducer[introducer] = len(leadsFromThisIntroducer)
        numOfSuccLeadsPerIntroducer[introducer] = len(clientsFromThisIntroducer)

        # Calculate successful PERCENTAGE for each introducer
        # Where successful PERCENTAGE is ((successfulLeads/leads)*100
    # Create a list with introducers who have successful percentage over 70%
    successPercentage = {}
    successfulIntroducers = {}
    for introducer in introducers:
        if numOfLeadsPerIntroducer[introducer] > 0:
            percentage = numOfSuccLeadsPerIntroducer[introducer] / numOfLeadsPerIntroducer[introducer] * 100.0
            successPercentage[introducer] = float("{0:.2f}".format(percentage))
        else:
            successPercentage[introducer] = 0
        if successPercentage[introducer] > 65:
            successfulIntroducers[introducer] = (successPercentage[introducer], numOfSuccLeadsPerIntroducer[introducer])

    # sucIntroPercenSorted has the successfull introducers sorted with the best first
    succIntroPercenSorted = OrderedDict(sorted(successfulIntroducers.items(), key=lambda v: v[1], reverse=True))

    # Calculate profit gained from each lead given from each introducer
    profits = {}
    profithours = {}
    for introducer in introducers:
        profits[introducer] = 0
    for introducer in introducers:
        clientsFromThisIntroducer = Person.objects.filter(isclient='1', leadfrom=introducer)
        hours = 0
        for person in clientsFromThisIntroducer:
            # General Business profits from this introducer
            genContracts = GeneralContract.objects.filter(client=person, cancelled=False)
            if genContracts:
                for contract in genContracts:
                    profit = generalContractProfit(contract)
                    profits[introducer] += (profit * contract.years)

            # Life Business profits from this introducer
            lifeContr = LifeContract.objects.filter(client=person, cancelled=False)

            if lifeContr:
                LifeProfits = {}
                for contract2 in lifeContr:
                    LifeProfits[contract2] = lifeContractProfit(contract2, contract2.client)
                    profit = LifeProfits[contract2]['total']
                    # sum up profit from this contract
                    profits[introducer] += profit
            # Get hours spent on person
            activities = Calendar.objects.filter(activity__customerid=person)
            for a in activities:
                hours += a.activity.duration
        profithours[introducer] = hours

    profitBased = {}
    for key in profits:
        if profits[key] != 0:
            profitBased[key] = profits[key]
    profitBasedSorted = OrderedDict(sorted(profitBased.items(), key=lambda x: x[1], reverse=True))

    successProfitHours = {}
    profitHoursDic = {}
    successProfitHoursSorted = {}
    for person in succIntroPercenSorted:
        successProfitHours[person] = {'percentage': succIntroPercenSorted[person],
                                      'hours': float("{0:.2f}".format(profithours[person] / 60))}
    successProfitHoursSorted = OrderedDict(
        sorted(successProfitHours.items(), key=lambda x: (-x[1]['percentage'][0], x[1]['hours'])))

    # Take first 20 people from successful Introducers
    finalProfitHours = {}
    if len(successProfitHoursSorted) > 20:
        for key in sorted(successProfitHoursSorted)[:20]:
            finalProfitHours[key] = successProfitHoursSorted[key]
    else:
        for key in sorted(successProfitHoursSorted):
            finalProfitHours[key] = successProfitHoursSorted[key]
    finalDicSorted = OrderedDict(
        sorted(finalProfitHours.items(), key=lambda x: (-x[1]['percentage'][0], x[1]['hours'])))

    for person in finalDicSorted:
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
        if person.occupation not in occupations:
            occupations[person.occupation] = 1
        else:
            occupations[person.occupation] += 1

    # Take introducers based on profit gained from leads
    for person in profitBasedSorted:
        profitHoursDic[person] = {'profit': profitBasedSorted[person],
                                  'hours': float("{0:.2f}".format(profithours[person] / 60))}
    profitHoursSortedIntro = OrderedDict(sorted(profitHoursDic.items(), key=lambda x: (-x[1]['profit'], x[1]['hours'])))

    # Take first 20 people from Introducers based on profit
    finalProfitBased = {}
    if len(profitHoursSortedIntro) > 20:
        for key in sorted(profitHoursSortedIntro)[:20]:
            finalProfitBased[key] = profitHoursSortedIntro[key]
    else:
        for key in sorted(profitHoursSortedIntro):
            finalProfitBased[key] = profitHoursSortedIntro[key]
    finalProfitBasedDicSorted = OrderedDict(
        sorted(finalProfitBased.items(), key=lambda x: (-x[1]['profit'], x[1]['hours'])))

    for person in finalProfitBasedDicSorted:
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
        if person.occupation not in occupations:
            occupations[person.occupation] = 1
        else:
            occupations[person.occupation] += 1

    averageAge = ageSum / (len(finalDicSorted) + len(finalProfitBasedDicSorted))
    averageAge = float("{0:.2f}".format(averageAge))
    occupBasedSorted = OrderedDict(sorted(occupations.items(), key=lambda x: x[1], reverse=True))
    if len(occupBasedSorted) > 4:
        occupBasedFinal = [k for k in sorted(occupBasedSorted.keys())[:4]]
    else:
        occupBasedFinal = [k for k in sorted(occupBasedSorted.keys())]

    genderAverage = ""
    if males > females:
        genderAverage = "Male"
    elif females > males:
        genderAverage = "Female"
    else:
        genderAverage = "Male/Female"

    return render(request, 'leadsMasterApp/iconicIntroducer.html',
                  {'genderAverage': genderAverage, 'minAge': minAge, 'maxAge': maxAge,
                   'averageAge': averageAge, 'finalDicSorted': finalDicSorted,
                   'introducers': introducers, 'finalProfitBasedDicSorted': finalProfitBasedDicSorted,
                   'occupBasedFinal': occupBasedFinal})


# Report: Iconic Client Profile
def IconicClientView(request):
    today = datetime.now()

    lifePlan = ""
    generalPlan = ""
    if request.method == "POST":
        plansForm = PlansOptionsForm(data=request.POST)
        if plansForm.is_valid():
            generalPlan = plansForm.cleaned_data['generalPlan']
            lifePlan = plansForm.cleaned_data['lifePlan']
    else:
        plansForm = PlansOptionsForm()

    if (lifePlan != "") or (generalPlan != ""):
        clients = Person.objects.filter(isclient=1)
        # Calculate profit gained from each lead given from each introducer
        profits = {}
        for client in clients:
            if (not lifePlan) and generalPlan:
                # General Business profits from this client
                genContracts = GeneralContract.objects.filter(client=client, cancelled=False, plan=generalPlan.planid)
                if genContracts:
                    if client not in profits:
                        profits[client] = 0
                    for contract in genContracts:
                        profit = generalContractProfit(contract)
                        profits[client] += (profit * (contract.years / 12))
            elif (not generalPlan) and lifePlan:
                # Life Business profits from this introducer
                lifeContr = LifeContract.objects.filter(client=client, cancelled=False, plan=lifePlan.planlifeid)
                if lifeContr:
                    if client not in profits:
                        profits[client] = 0
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
                    profits[client] += (profit * (contract.years / 12))

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
    averageAge = 0
    genderAverage = ""
    occupBasedFinal = "-"
    profitHours = {}
    profitHoursSorted = {}
    if profitSorted:
        for person in profitSorted:
            # Get hours spent on person
            hours = 0
            activities = Calendar.objects.filter(activity__customerid=person)
            for a in activities:
                hours += a.activity.duration
            profitHours[person] = {'profit': float("{0:.2f}".format(profitSorted[person])),
                                   'hours': float("{0:.2f}".format(hours / 60))}

        profitHoursSorted = OrderedDict(sorted(profitHours.items(), key=lambda x: (-x[1]['profit'], x[1]['hours'])))
        finalDic = {}
        if len(profitHoursSorted) > 20:
            for key in sorted(profitHoursSorted)[:20]:
                finalDic[key] = profitHoursSorted[key]
        else:
            for key in sorted(profitHoursSorted):
                finalDic[key] = profitHoursSorted[key]
        finalDicSorted = OrderedDict(sorted(finalDic.items(), key=lambda x: (-x[1]['profit'], x[1]['hours'])))

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
    return render(request, 'leadsMasterApp/iconicClient.html',
                  {'genderAverage': genderAverage, 'minAge': minAge, 'maxAge': maxAge,
                   'averageAge': averageAge, 'clients': clients,
                   'finalDicSorted': finalDicSorted,
                   'occupBasedFinal': occupBasedFinal,
                   'plansForm': plansForm})


# Report: Payments Report
def paymentsReportView(request):
    today = datetime.now()

    toBePaidGeneral = {}
    toBePaidLife = {}
    upcomingGeneral = {}
    upcomingLife = {}
    # Filter past payments
    for item in GeneralContract.objects.filter(nextpayment__lte=today.date(), cancelled=False):
        contract = item
        nextPayment = float("{0:.2f}".format(contract.annualpremium / int(contract.doses)))
        toBePaidGeneral[contract] = nextPayment
    for item in LifeContract.objects.filter(nextpayment__lte=today.date(), cancelled=False):
        contract = item
        nextPayment = float("{0:.2f}".format(contract.annualpremium / int(contract.doses)))
        toBePaidLife[contract] = nextPayment

    # Filter future payments due in 5 days
    for item in GeneralContract.objects.filter(
            nextpayment__range=[(today.date() + timedelta(days=1)), (today.date() + timedelta(days=6))],
            cancelled=False):
        contract = item
        nextPayment = float("{0:.2f}".format(contract.annualpremium / int(contract.doses)))
        upcomingGeneral[contract] = nextPayment
    for item in LifeContract.objects.filter(
            nextpayment__range=[(today.date() + timedelta(days=1)), (today.date() + timedelta(days=6))],
            cancelled=False):
        contract = item
        nextPayment = float("{0:.2f}".format(contract.annualpremium / int(contract.doses)))
        upcomingLife[contract] = nextPayment
    return render(request, 'leadsMasterApp/paymentsPage.html', {'toBePaidLife': toBePaidLife,
                                                                'toBePaidGeneral': toBePaidGeneral,
                                                                'upcomingGeneral': upcomingGeneral,
                                                                'upcomingLife': upcomingLife})


# This function calculates The Successful Percentage of Leads given from an introducer
def successfulLeadsPercentage(introducer):
    numOfLeads = 0
    numOfSuccLeads = 0
    leadsFromIntroducer = Person.objects.filter(leadfrom=introducer.id)
    # Calculate
    for person in leadsFromIntroducer:
        numOfLeads += 1
        if person.isclient == 1:
            numOfSuccLeads += 1
            # Calculate successful PERCENTAGE
            # Where successful PERCENTAGE is ((leads-successfulLeads)/leads)*100
    if numOfSuccLeads > 0:
        percentage = numOfSuccLeads / numOfLeads * 100.0
    else:
        percentage = 0
    percentage = float("{0:.2f}".format(percentage))

    return percentage