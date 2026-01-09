from django.contrib import admin
from .models import Medication, Documents,PatientUser
#,Appointment


admin.site.register(Medication)
admin.site.register(Documents)
admin.site.register(PatientUser)
#admin.site.register(Appointment)


