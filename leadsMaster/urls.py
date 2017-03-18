from django.conf.urls import url
from django.contrib import admin
from leadsMasterApp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.IndexView, name='index'),

    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^calendar/(?P<day>\w+)/(?P<month>\w+)/(?P<year>\w+)/$',views.calendar, name = 'calendarDay'),
    url(r'^calendar/(?P<pkc>\d+)/$',views.edit_Calendar_Entry, name='editCalendarEntry'),

    url(r'^ourPeople/$', views.OurPeopleView, name='ourPeople'),
    url(r'^ourPeople/new$', views.AddProfileView, name='addProfile'),
    url(r'^ourPeople/(?P<pk>\d+)/edit/$', views.EditProfileView, name='editProfile'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView, name='ProfileView'),

    url(r'^companies/$', views.CompaniesView, name='companies'),
    url(r'^companies/(?P<pk>\d+)/editCompany$', views.EditCompanyView, name='editCompany'),
    url(r'^companies/addCompany$', views.AddCompanyView, name='addCompany'),
    url(r'^companies/addGenPlan/(?P<pk>\d+)/editGenPlan$', views.EditGenPlanView, name='editGenPlan'),
    url(r'^companies/addGenPlan$', views.AddGenPlanView, name='addGenPlan'),
    url(r'^companies/addLifePlan$', views.AddLifePlanView, name='addLifePlan'),
    url(r'^companies/addLifePlan/(?P<pk>\d+)/editLifePlan$', views.EditLifePlanView, name='editLifePlan'),

    url(r'^reports/$', views.ReportsView, name='reports'),
    url(r'^reports/iconicIntroducer$', views.IconicIntroducerView, name='iconicIntroducer'),
    url(r'^reports/iconicClient$', views.IconicClientView, name='iconicClient'),
    url(r'^reports/manHours$', views.ManHoursView, name='manHours'),
    url(r'^reports/manHours/(?P<pk>\d+)/$', views.ManHoursPersonView, name='manHoursPerson'),
    url(r'^reports/succLeads$', views.SuccLeadsView, name='succLeads'),
    url(r'^reports/succLeads/(?P<pk>\d+)/$', views.succLeadsPersonView, name='succLeadsPerson'),
    url(r'^reports/salesReport$', views.salesReportsView, name='salesReport'),
    url(r'^reports/paymentsReport$', views.paymentsReportView, name='paymentsReport'),

    url(r'^register/$', views.register, name='register'),
    url(r'^registerAdmin/$', views.registerAdmin, name='registerAdmin'),
    url(r'^login/$', views.user_login , name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^addContractLife/$', views.addContractLifeView, name='addContractLife'),
    url(r'^editContractLife/(?P<pk>\d+)/$', views.editContractLifeView, name='editContractLife'),
    url(r'^addContractGeneral/$', views.addContractGeneralView, name='addContractGeneral'),
    url(r'^editContractGeneral/(?P<pk>\d+)/$', views.editContractGeneralView, name='editContractGeneral'),
    url(r'^contract/(?P<pk>\w+)/(?P<type>\w+)$', views.ContractPageView, name='contractPage'),

]
