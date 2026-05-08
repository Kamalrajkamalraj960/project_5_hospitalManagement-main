from django.contrib import admin
from django.contrib import admin
from .models import Department
from .models import Doctors
from .models import Booking


# Register your models here.
admin.site.register(Department)
admin.site.register(Doctors)
admin.site.register(Booking)

