from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from patients import views as patient_views
from django.contrib.auth import views as auth_views

app_name = 'patient'

urlpatterns = [
    path('', views.home, name='patient-home'),
    path('medication/', patient_views.UploadMedication.as_view(), name='medupload'),
    path('documents/', patient_views.UploadDocuments.as_view(), name='docupload'),
    path('share/', views.share_documents, name='sharedoc'),
    path('profile/',patient_views.view_profile,name = 'patprofile'),
    path('register/',patient_views.RegisterPatient,name = 'RegisterPatient'),
    path('prescription/', views.view_prescription, name='view_prescription'),
    path('scans/', views.view_scans, name='view_scans'),
    path('labreports/', views.view_lab, name='view_lab'),
    path('appointments/',views.view_appointments,name='appointments'),
    path('certificates/', views.view_certificate, name='view_certificate'),
    path('available-doctors/', views.view_doctors, name='available_doctors'),
    path('delete-medication/<int:medication_id>/', patient_views.DeleteMedication.as_view(), name='delete_medication'),  # Add this line
    path('delete-prescription/<int:Documents_id>/', patient_views.DeletePrescription.as_view(), name='delete_prescription'),
    path('delete-lab/<int:lab_id>/', patient_views.DeleteLab.as_view(), name='delete_lab'),
    path('delete-scan/<int:scan_id>/', patient_views.DeleteScans.as_view(), name='delete_scans'),
    path('delete-certificate/<int:certificate_id>/', patient_views.DeleteCertificates.as_view(), name='delete_certificates'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
