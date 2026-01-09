from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from doctors.models import DoctorUser,Profile


def home(request):
    return render(request, 'loginorreg.html')

def land(request):
    return render(request,'home.html')

@login_required
def profile(request,doctor_id):
   doctor = get_object_or_404(DoctorUser, user__username=doctor_id)
   profile = Profile.objects.get(doctor_user=doctor)

   context={
       'profile':profile,
   }
   return render(request,'profile.html',context)




