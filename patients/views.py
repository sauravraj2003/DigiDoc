from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Medication, Documents,PatientUser
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import PatientRegisterForm, DocumentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from doctors.models import DoctorUser, SharedDocument,Appointment
from django.contrib.auth.mixins import LoginRequiredMixin
from doctors.models import Profile,DoctorUser
from django.contrib import messages
@login_required
def home(request):
     user = request.user
     if PatientUser.objects.filter(user=user).exists():
      return render(request, 'patients/pathome.html')
     else:
         return redirect('home')


def RegisterPatient(request):
    if request.method=="POST":
         form = PatientRegisterForm(request.POST)
         if form.is_valid():
             user_instance = form.save()
             patient_user = PatientUser.objects.create(user=user_instance,phone_number = form.cleaned_data['phone_number'],age = form.cleaned_data['age'],name = form.cleaned_data['name'],gender = form.cleaned_data['gender'],blood_group = form.cleaned_data['blood_group'])
             #messages.success(request,f'Account created for {username}')
             return redirect('home')
    else:
         form = PatientRegisterForm()
    return render(request,'patients/patientreg.html',{'form':form})

"""
@login_required
def redirect_user(request):
    user = request.user

    # Check if the user is a doctor
    if PatientUser.objects.filter(user=user).exists():
        return render(request,'patients/pathome.html')

    # If user is not a doctor or patient, redirect to a generic dashboard or homepage
    else:
        return redirect('home')
"""

class DeleteMedication(View):
    def delete(self, request, medication_id):
        try:
            medication = Medication.objects.get(pk=medication_id)
            medication.delete()
            return JsonResponse({'message': 'Medication deleted successfully'})
        except Medication.DoesNotExist:
            return JsonResponse({'error': 'Medication not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class DeletePrescription(View):
    def delete(self, request, Documents_id):
        try:
            medication = Documents.objects.get(pk=Documents_id)
            medication.delete()
            return JsonResponse({'message': 'Medication deleted successfully'})
        except Documents.DoesNotExist:
            return JsonResponse({'error': 'Medication not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class DeleteLab(View):
    def delete(self, request, lab_id):
        try:
            lab = Documents.objects.get(pk=lab_id)
            lab.delete()
            return JsonResponse({'message': 'Lab report deleted successfully'})
        except Documents.DoesNotExist:
            return JsonResponse({'error': 'Lab report not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class DeleteScans(View):
    def delete(self, request, scan_id):
        try:
            lab = Documents.objects.get(pk=scan_id)
            lab.delete()
            return JsonResponse({'message': 'Scans deleted successfully'})
        except Documents.DoesNotExist:
            return JsonResponse({'error': 'Scans not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class DeleteCertificates(View):
    def delete(self, request, certificate_id):
        try:
            lab = Documents.objects.get(pk=certificate_id)
            lab.delete()
            return JsonResponse({'message': 'Medical Certificates deleted successfully'})
        except Documents.DoesNotExist:
            return JsonResponse({'error': 'Medical Certificates not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class UploadMedication(LoginRequiredMixin, CreateView):
    model = Medication
    fields = ['medical_condition', 'medicines', 'file','document_name','comments']
    success_url = reverse_lazy('patient:medupload')
    login_url = '/patient/login/' 
    
    def form_valid(self, form):
        form.instance.author = self.request.user.patientuser
        sample=Documents.objects.filter(author=self.request.user.patientuser,document_name=form.instance.document_name,type='prescription').exists()
        if(sample):
            messages.error(self.request, "A prescription with the same name already exists.")
            return redirect('patient:patient-home')
        Documents.objects.create(
            author=self.request.user.patientuser,
            file=form.instance.file,
            document_name=form.instance.document_name,
            type='prescription',
            comments=form.instance.comments
            

        )
        # Documents.objects.create(
        #     author=self.request.user.patientuser,
        #     file=form.instance.file,
        #     document_name=form.instance.document_name,
        #     type='current'
        # )
        response = super().form_valid(form)
        reset_form_script = "<script>resetForm();</script>"
        response.content += reset_form_script.encode()
        return response

    def get_context_data(self, **kwargs):
        patient = self.request.user.patientuser
        context = super().get_context_data(**kwargs)
        context['medications'] = Medication.objects.filter(author = patient)
        return context
    
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Documents
from .forms import DocumentForm

class UploadDocuments(LoginRequiredMixin, CreateView):
    model = Documents
    form_class = DocumentForm
    success_url = reverse_lazy('patient:docupload')
    login_url = '/patient/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user.patientuser
        
        # Check if a document with the same name and type already exists
        document_name = form.cleaned_data['document_name']
        document_type = form.cleaned_data['type']
        existing_document = Documents.objects.filter(author=self.request.user.patientuser, document_name=document_name, type=document_type,verified=False).exists()
        
        if existing_document:
            self.duplicate_document = True
            messages.error(self.request, "A document with the same name already exists.")
            return redirect('patient:patient-home')
              # Return form invalid if duplicate document found
        else:
            self.duplicate_document = False
            
            return super().form_valid(form)  # Proceed with form submission if no duplicates

    def get_context_data(self, **kwargs):
        patient = self.request.user.patientuser
        context = super().get_context_data(**kwargs)
        context['documents'] = Documents.objects.filter(author=patient)
        context['duplicate_document'] = getattr(self, 'duplicate_document', False)
        return context


    
@login_required
def share_documents(request):
    user = request.user
    if not PatientUser.objects.filter(user=user).exists():
        return redirect('login')
    patient = request.user.patientuser
    documents = Documents.objects.filter(author=patient)
    doctors = DoctorUser.objects.filter(profile__isnull=False)

    if request.method == 'POST':
        selected_doctors = request.POST.getlist('doctors')
        selected_documents = request.POST.getlist('documents')

        for doctor_id in selected_doctors:
            doctor = DoctorUser.objects.get(id=doctor_id)
            for document_id in selected_documents:
                document = Documents.objects.get(id=document_id, author=patient)
                existing_document = SharedDocument.objects.filter(patient = patient, document=document_id, doctor=doctor,verified=False).exists()
        
                if existing_document:
                #   self.duplicate_document = True
                  messages.error(request, "Document is already shared with Doctor.")
                  return redirect('patient:patient-home')
                else:
                   SharedDocument.objects.create(document_name=document.document_name,document=document, doctor=doctor, patient=patient)
                   messages.success(request, 'Files shared successfully!')
        # Add success message
       

        return redirect('patient:patient-home')

    return render(request, 'patients/share_documents.html', {'documents': documents, 'doctors': doctors})


#cretae a view to only showcasse documents with type prescriptio

@login_required
def view_prescription(request):
    user = request.user
    if not PatientUser.objects.filter(user=user).exists():
        return redirect('login')
    patient = request.user.patientuser
    prescriptions = Documents.objects.filter(author=patient, type='prescription')
    context = {'prescriptions': prescriptions}
    return render(request, 'patients/view_prescription.html', context)

@login_required
def view_doctors(request):
    user = request.user
    if not PatientUser.objects.filter(user=user).exists():
        return redirect('login')
    
    doctor_profiles = Profile.objects.all()
    
    # Pass the doctor profiles to the template for rendering
    return render(request, 'patients/available_doctors.html', {'doctor_profiles': doctor_profiles})

@login_required
def view_scans(request):
    user = request.user
    if not PatientUser.objects.filter(user=user).exists():
        return redirect('login')
    patient = request.user.patientuser
    scans = Documents.objects.filter(author=patient, type='scans')
    context = {'scans': scans}
    return render(request, 'patients/view_scans.html', context)

@login_required
def view_lab(request):
    user = request.user
    if not PatientUser.objects.filter(user=user).exists():
        return redirect('login')
    patient = request.user.patientuser
    lab = Documents.objects.filter(author=patient, type='lab_report')
    context = {'lab': lab}
    return render(request, 'patients/view_lab.html', context)

@login_required
def view_certificate(request):
    user = request.user
    if not PatientUser.objects.filter(user=user).exists():
        return redirect('login')
    patient = request.user.patientuser
    certificate = Documents.objects.filter(author=patient, type='medical_certificate')
    context = {'certificate': certificate}
    return render(request, 'patients/view_certificate.html', context)


from django.utils import timezone
from datetime import timedelta
@login_required
def view_appointments(request):
    user = request.user
    if not PatientUser.objects.filter(user=user).exists():
        return redirect('login')
    
    patient = request.user.patientuser
    
    # Calculate the current time plus 30 minutes
    current_time_plus_30_min = timezone.now() + timedelta(minutes=30)
    
    # Retrieve appointments of the patient that are scheduled 30 minutes or more in the future
    appointments = Appointment.objects.filter(patient=patient, date__gte=current_time_plus_30_min)
    
    context = {'appointments': appointments}
    return render(request, 'patients/appointments.html', context)

@login_required
def view_profile(request):
    user = request.user
    if not PatientUser.objects.filter(user=user).exists():
        return redirect('login')
    patient = request.user.patientuser
    context = {'patient' : patient}
    return render(request,'patients/patprofile.html',context)