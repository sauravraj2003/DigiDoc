from django import forms
from django.contrib.auth.models import User
from .models import PatientUser, Documents
from django.contrib.auth.forms import UserCreationForm

class PatientRegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField()
    phone_number = forms.IntegerField(max_value=9999999999, min_value=1000000000)
    age = forms.IntegerField(max_value=200, min_value=0)
    gender = forms.ChoiceField(label='Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    blood_group = forms.ChoiceField(label='Blood Group',choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'),('O+', 'O+'), ('O-', 'O-')])
   

    class Meta:
        model=User
        fields= ['username','name','phone_number','email','password1','password2','gender','age', 'blood_group']
    

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['file', 'type', 'document_name','comments']