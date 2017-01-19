from django.contrib import admin
from .models import Activity, birthdayNot, genRenewalsNot, genPaymentsNot, lifeRenewalsNot, lifePaymentsNot
from .models import Calendar
from .models import Company
from .models import GeneralContract
from .models import LifeContract
from .models import Employee
from .models import Generalbusinessplans
from .models import Lifebusinessplans
from .models import Person
from .models import UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Activity)
admin.site.register(Calendar)
admin.site.register(Company)
admin.site.register(GeneralContract)
admin.site.register(LifeContract)
admin.site.register(Employee)
admin.site.register(Generalbusinessplans)
admin.site.register(Lifebusinessplans)
admin.site.register(Person)
admin.site.register(birthdayNot)
admin.site.register(genRenewalsNot)
admin.site.register(lifeRenewalsNot)
admin.site.register(genPaymentsNot)
admin.site.register(lifePaymentsNot)


