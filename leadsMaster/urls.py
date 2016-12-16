"""leadsMaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from leadsMasterApp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.IndexView, name='index'),
    url(r'^birthdays$', views.IndexBirthdayView, name='indexBirthday'),
    url(r'^todo$', views.IndexToDoView, name='indexToDo'),
    url(r'^renewals$', views.IndexRenewalsView, name='indexRenewals'),
    url(r'^payments$', views.IndexPaymentsView, name='indexPayments'),
    url(r'^leadsToContact$', views.IndexLeadsToContactView, name='indexLeadsToContact'),
    url(r'^calendar/$', views.CalendarView, name='calendar'),
    url(r'^ourPeople/$', views.OurPeopleView, name='ourPeople'),
    url(r'^ourPeople/new$', views.AddProfileView, name='addProfile'),
    url(r'^ourPeople/(?P<pk>\d+)/edit/$', views.EditProfileView, name='editProfile'),
    url(r'^reports/$', views.ReportsView, name='reports'),
    url(r'^reports/iconicIntroducer$', views.IconicIntroducerView, name='iconicIntroducer'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login , name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^addContract/$', views.addContractView, name='addContract'),

]
