from django.urls import path
from .views import *


appointment_list = AppointementViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
appointment_detail = AppointementViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('register', register_patient, name='patient-registration'),
    path('email-verify',email_verify, name='email_verify'),
    path('patient/profile', patient_profile, name='patient-profile'),
    path('patient/appointments', appointment_list, name='patient-appointment'),
    path('patient/appointments/<int:pk>', appointment_detail, name='patient-appointment-detail'),
    path('patient/appointments/<status>', appointment_status, name='patient-appointment-status'),
    path('patient/prescriptions', prescription_list, name='prescription-list'),
    path('patient/prescriptions/<int:pk>', prescription_detail, name='prescription-detail'),
]