from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers, status, viewsets
from doctor.models import Doctor
from rest_framework.permissions import BasePermission

from patient.models import Appointment, Patient
from doctor.models import Doctor
# from patient.serializers import PatientSerializer
# from doctor.serializers import DoctorSerializer

from .serializers import (
    PatientSerializer, 
    DoctorSerializer, 
    AppointmentSerializer
)

class IsReception(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsReception]
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()


class DoctorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsReception]
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()


class AppointementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsReception]
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()




    # def get_queryset(self):
    #     patient = Patient.objects.get(user=self.request.user)
    #     appointments = Appointment.objects.filter(patient=patient)
    #     return appointments   

    # def perform_create(self, serializer):
    #     patient = Patient.objects.get(user=self.request.user)
    #     serializer.save(patient=patient)  

# @api_view(['GET'])
# def patient_list(request):
#     patient = Patient.objects.all()
#     serializer = PatientSerializer(patient, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def doctor_list(request):
#     doctor = Doctor.objects.all()
#     serializer = DoctorSerializer(doctor, many=True)
#     return Response(serializer.data)



