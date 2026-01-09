from django.db import models
from django.contrib.auth.models import User


class PatientUser(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    age = models.IntegerField(default=0)
    USERNAME_FIELD = 'username'
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices, default=('male', 'Male'))
    blood_group_choices = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=3, choices=blood_group_choices, default=('A+', 'A+'))

class Medication(models.Model):
    medical_condition = models.CharField(max_length=100)
    medicines = models.TextField()
    author = models.ForeignKey(PatientUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='') 
    document_name = models.CharField(max_length=100)
    comments = models.CharField(max_length=500,default = 'None')

class Documents(models.Model):
    DOCUMENT_TYPES = (
    ('prescription', 'Prescription'),
    ('lab_report', 'Lab Report'),
    ('scans', 'Scans'),
    ('medical_certificate', 'Medical Certificate'),
    
)
    author = models.ForeignKey(PatientUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='')
    type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default = 'prescription')
    document_name = models.CharField(max_length=100)
    comments = models.CharField(max_length=500,default = 'None')
    verified = models.BooleanField(default=False)



   
