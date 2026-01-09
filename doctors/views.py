from django.shortcuts import render,redirect
from .models import Prescription,DoctorUser,SharedDocument,Profile,Appointment,Day
from patients.models import PatientUser
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import DoctorRegisterForm,ProfileUpdateForm,ScheduleAppointment,DocumentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

@login_required
def home(request):
    user = request.user
    if not DoctorUser.objects.filter(user=user).exists():
        return redirect('login')
    doctor = request.user.doctoruser
    shared_docs = SharedDocument.objects.filter(doctor=doctor)
    shared_patients = set([doc.patient for doc in shared_docs])

    context = {
        'shared_docs': shared_docs,
        'shared_patients': shared_patients,
        'user': user,
    }
    
    return render(request, 'doctors/dochome.html', context)
# @login_required
# def home(request):
#      user = request.user
#      if DoctorUser.objects.filter(user=user).exists():
#       return render(request, 'doctors/dochome.html')
#      else:
#          return redirect('home')


def RegisterDoc(request):
    if request.method=="POST":
         form = DoctorRegisterForm(request.POST,request.FILES)
         if form.is_valid():
             user_instance = form.save()
             selected_days=Day.objects.all()
             doctor_user = DoctorUser.objects.create(user=user_instance,license=form.cleaned_data['license'],phone_number = form.cleaned_data['phone_number'],name = form.cleaned_data['name'])
             profile = Profile.objects.create(doctor_user=doctor_user,specialization="none",hospital="none")
             profile.working_days.set(selected_days)
             #messages.success(request,f'Account created for {username}')
             return redirect('home')
    else:
         form = DoctorRegisterForm()
    return render(request,'doctors/DocRegister.html',{'form':form})

@login_required
def redirect_user(request):
    user = request.user

    # Check if the user is a doctor
    if DoctorUser.objects.filter(user=user).exists():
        # return render(request,'doctors/Dochome.html')
        return redirect('doctor:doctor-home')
    elif PatientUser.objects.filter(user=user).exists():
        # return render(request,'patients/pathome.html')
        return redirect('patient:patient-home')
    # If user is not a doctor or patient, redirect to a generic dashboard or homepage
    else:
        return redirect('home')

class UploadPrescription(LoginRequiredMixin, CreateView):
    model = Prescription
    fields = ['patientName', 'patientID', 'followUpDate', 'file',]
    success_url = reverse_lazy('presupload')
    login_url = '/doctor/login/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user.doctoruser
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prescriptions'] = Prescription.objects.all()
        return context
    

# @login_required
# def shared_documents(request):
#     doctor = request.user.doctoruser
#     shared_docs = SharedDocument.objects.filter(doctor=doctor)
#     return render(request, 'doctors/shared_documents.html', {'shared_docs': shared_docs})

@login_required
def shared_documents(request):
    user = request.user
    if not DoctorUser.objects.filter(user=user).exists():
        return redirect('login')
    doctor = request.user.doctoruser
    shared_docs = SharedDocument.objects.filter(doctor=doctor)
    shared_patients = set([doc.patient for doc in shared_docs])

    context = {
        'shared_patients': shared_patients,
        'shared_docs': shared_docs,
    }

    return render(request, 'doctors/shared_documents.html', context)


from django.contrib import messages

@login_required
def patient_documents(request, patient_username):
    patient = get_object_or_404(PatientUser, user__username=patient_username)
    doctor = request.user.doctoruser
    shared_docs = SharedDocument.objects.filter(patient=patient, doctor=doctor)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document_type = form.cleaned_data['type']
            document_name = form.cleaned_data['document_name']
            document_comments=form.cleaned_data['comments']
            # Check if a document with the same name and type already exists
            if shared_docs.filter(document__document_name=document_name, document__type=document_type,verified=True).exists():
                messages.error(request, "Document with the same name and type already exists.")
                return redirect('doctor:doctor-home')
            else:
                document = form.save(commit=False)
                document.author = patient
                document.save()
                SharedDocument.objects.create(document=document, doctor=doctor, patient=patient, document_name=document_name, verified=True,comments=document_comments)
                return redirect('doctor:patient_documents', patient_username=patient_username)
    else:
        form = DocumentForm()

    context = {
        'patient': patient,
        'shared_docs': shared_docs,
        'form': form,
    }

    return render(request, 'doctors/patient_documents.html', context)





@login_required
def updateform(request):
    user = request.user
    if not DoctorUser.objects.filter(user=user).exists():
        return redirect('login')

    doctor = DoctorUser.objects.get(user=user)
    profile = Profile.objects.get(doctor_user=doctor)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('doctor:doctor-home')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'doctors/update.html',{'form':form})


from django.utils import timezone
from datetime import timedelta
@login_required
def appointments(request):
    # Get the currently logged-in doctor user
    doctor = request.user.doctoruser

    # Calculate the current time plus 30 minutes
    current_time_plus_30_min = timezone.now() - timedelta(minutes=30)

    # Retrieve appointments of the doctor that are scheduled 30 minutes or more in the future
    appointments = Appointment.objects.filter(doctor=doctor, date__gte=current_time_plus_30_min)

    # Render the template and pass the filtered appointments as context
    return render(request, 'doctors/view_current_appointments.html', {'appointments': appointments})

    


from django.core.exceptions import ValidationError
from .models import DAYS_OF_WEEK
from django.utils import timezone
from datetime import datetime
@login_required
def Schedule(request, patient_id):
    user = request.user
    current_system_datetime = timezone.now()
    print(current_system_datetime)  # Print the current system datetime
    current_system_datetime_str = current_system_datetime.strftime('%Y-%m-%d %H:%M')
    if not DoctorUser.objects.filter(user=user).exists():
        return redirect('login')

    current_doctor = request.user.doctoruser
    current_patient = get_object_or_404(PatientUser, user__username=patient_id)

    if request.method == "POST":
        form = ScheduleAppointment(request.POST)
        if form.is_valid():
            follow_up_date = form.cleaned_data['FollowUpDate']
            min_follow_up_time = follow_up_date - timezone.timedelta(minutes=30)
            max_follow_up_time = follow_up_date + timezone.timedelta(minutes=30)
            if follow_up_date < current_system_datetime:
                messages.error(request, "The date entered is in the past")
                return redirect('doctor:doctor-home')
            # Check if there's already an appointment within 30 minutes
            overlapping_appointments = Appointment.objects.filter(doctor=current_doctor, date__range=(min_follow_up_time, max_follow_up_time))
            if overlapping_appointments.exists() and not overlapping_appointments.filter(patient=current_patient).exists():
                messages.error(request, "Another appointment already exists within 30 minutes of this time.")
                return redirect('doctor:doctor-home')
            
            # Check if the appointment falls on a working day for the doctor
            appointment_day = follow_up_date.strftime('%A')  # Get the day name from the date
            if not current_doctor.profile.working_days.filter(name=appointment_day).exists():
                messages.error(request, "Appointment date does not fall on a working day for the doctor.")
                return redirect('doctor:doctor-home')
            
            # Delete all existing appointments for the current patient and doctor
            existing_appointments = Appointment.objects.filter(patient=current_patient, doctor=current_doctor)
            existing_appointments.delete()

            # Create a new appointment
            Appointment.objects.create(patient=current_patient, doctor=current_doctor, date=follow_up_date)
            
            return redirect('doctor:doctor-home')
    else:
        form = ScheduleAppointment()

    return render(request, 'doctors/appointmentadd.html', {'form': form})






from django.http import JsonResponse

# @login_required
# def delete_shared_documents(request):
#     if request.method == 'POST' and request.is_ajax():
#         try:
#             patient_name = request.POST.get('patient_name')

#             # Delete shared documents associated with the patient's name
#             SharedDocument.objects.filter(patient__name=patient_name).delete()

#             return JsonResponse({'message': 'Shared documents deleted successfully'}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)