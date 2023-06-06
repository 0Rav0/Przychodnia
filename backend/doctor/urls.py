from .views import *
from django.urls import path, include


appointment_list = AppointementViewSet.as_view({
    'get': 'list'
})
appointment_detail = AppointementViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})


urlpatterns = [
    path('list', doctor_list, name='doctor-list'),
    path('profile', doctor_profile, name='doctor-profile'),
    path('appointments',appointment_list, name='appointment-list'),
    path('appointments/<int:pk>', appointment_detail, name='appointment-detail'),
    path('appointments/<int:pk>/patient', get_appointment_patient_detail, name='appointment-patient-detail'),
]