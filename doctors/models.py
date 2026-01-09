from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from patients.models import PatientUser, Documents


class DoctorUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null = True)
    name = models.CharField(max_length=100)
    license = models.FileField()
    phone_number = models.IntegerField()
    USERNAME_FIELD = 'username'

class Prescription(models.Model):
    patientName = models.CharField(max_length=100)
    patientID = models.CharField(max_length=100)
    author = models.ForeignKey(DoctorUser, on_delete=models.CASCADE)
    followUpDate = models.DateField()
    file = models.FileField(upload_to='')
    
class SharedDocument(models.Model):
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    comments = models.CharField(max_length=500,default = 'None')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the verified field of the related Documents instance
        self.document.verified = self.verified
        self.document.save()
    

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)

class Day(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Profile(models.Model):
    doctor_user = models.OneToOneField(DoctorUser, on_delete=models.CASCADE, related_name='profile')
    specialization = models.CharField(max_length=100)
    hospital = models.CharField(max_length=100)
    working_days = models.ManyToManyField(Day)

class Appointment(models.Model):
    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE,null = True)
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        ordering = ['-date']  # Display appointments with the latest added appointment first

    def __str__(self):
        return f'{self.date.strftime("%d/%m/%Y %H:%M")}'   

    


