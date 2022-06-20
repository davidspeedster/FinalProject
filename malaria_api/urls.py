from django.contrib import admin
from django.urls import path, include
from malaria_api import views
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings

app_name = 'malaria_api'

urlpatterns = [
    #     path('admin/', admin.site.urls),
    path('hospital/', views.HospitalList.as_view(), name='create_hospital_list'),
    path('doctor/', views.DoctorList.as_view(), name='get_doctor_list'),
    path('registered_personnel/', views.RegisteredPersonnelList.as_view(),
         name='create_registered_personnel_list'),
    path('request_diagnostic/', views.RequestDiagnosticList.as_view(),
         name='create_request_diagnostic_list'),
    path('patient/', views.ReceptionistPatientList.as_view(),
         name='create_patient_list'),
    path('prescription/', views.PrescriptionList.as_view(),
         name='create_prescription_list'),
    path('hospital/<uuid:pk>', views.HospitalDetail.as_view(),
         name='create_hospital_detail_list'),
    path('registered_personnel/<uuid:pk>', views.RegisteredPersonnelDetail.as_view(),
         name='registered_personnel_detail_list'),
    path('request_diagnostic/<uuid:pk>', views.RequestDiagnosticDetail.as_view(),
         name='request_diagnostic_detail'),
    path('request_diagnostic/<uuid:pk>', views.SetDiagnosticResult.as_view(),
         name='request_diagnostic_detail'),
    path('patient/<uuid:pk>', views.ReceptionistPatientDetail.as_view(),
         name='create_patient_detail_list'),
    path('prescription/<uuid:pk>', views.PrescriptionDetail.as_view(),
         name='create_prescription_detail_list'),
    path('receptionist_patient_list/', views.ReceptionistPatientList.as_view(),
         name='create_prescription_detail_list'),
    path('receptionist_patient_detail/<uuid:pk>', views.ReceptionistPatientDetail.as_view(),
         name='create_prescription_detail_list'),
    path('doctor_patient_list/', views.DoctorPatientList.as_view(),
         name='create_prescription_detail_list'),
    path('doctor_patient_detail/<uuid:pk>', views.DoctorPatientDetail.as_view(),
         name='create_prescription_detail_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
