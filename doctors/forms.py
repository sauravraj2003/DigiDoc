from django import forms
from django.contrib.auth.models import User
from .models import DoctorUser,Appointment
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Day
from patients.models import PatientUser, Documents

class DoctorRegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField()
    phone_number = forms.IntegerField(max_value=9999999999, min_value=1000000000)
    license = forms.FileField()

    class Meta:
        model=User
        fields= ['username','name','phone_number','email','password1','password2','license']

class ProfileUpdateForm(forms.ModelForm):
     specialization = forms.CharField()
     hospital = forms.CharField()
     working_days = forms.ModelMultipleChoiceField(queryset=Day.objects.all(), widget=forms.CheckboxSelectMultiple)
     class Meta:
         model=Profile
         fields= ['specialization','hospital','working_days']

class ScheduleAppointment(forms.ModelForm):
    FollowUpDate = forms.DateTimeField()

    class Meta:
        model=Appointment
        fields = ['FollowUpDate']
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['file', 'type','document_name','comments']
    