from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import BasePermission

from patient.models import Appointment, Patient
from patient.serializers import PatientProfileSerializer

from .models import Doctor
from .serializers import *


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='doctor').exists())


@api_view(['GET'])
def doctor_list(request):
    doctor = Doctor.objects.all()
    serializer = DoctorSerializer(doctor, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def doctor_detail(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    serializer = DoctorSerializer(doctor, many=False)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsDoctor])
def doctor_profile(request, format=None):
    user = request.user

    if request.method == 'GET':
        profile = Doctor.objects.get(user=user)
        userSerializer=UserSerializer(user)
        profileSerializer = DoctorSerializer(profile)

        return Response({ 
            'user_data':userSerializer.data,
            'profile_data':profileSerializer.data

        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        profile = Doctor.objects.get(user=user)
        profileSerializer = DoctorSerializer(instance=profile, data=request.data.get('profile_data'))

        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({'profile_data':profileSerializer.data}, status=status.HTTP_200_OK)
        return Response({'profile_data':profileSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        profile = Doctor.objects.get(user=user)
        profileSerializer = DoctorSerializer(instance=profile, data=request.data.get('profile_data'), partial=True)

        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({'profile_data':profileSerializer.data}, status=status.HTTP_200_OK)
            
        return Response({'profile_data':profileSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AppointementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = AppointmentSerializer
    

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        appointments = Appointment.objects.filter(doctor=doctor)
        return appointments


@api_view(['GET'])
@permission_classes([IsDoctor])
def get_appointment_patient_detail(request, pk):
    user = request.user
    doctor = Doctor.objects.get(user=user)

    appointment = Appointment.objects.get(pk=pk)

    patient = appointment.patient
    patient_data = Patient.objects.get(pk=patient.id)
    patient_appointments = Appointment.objects.filter(patient=patient, doctor=doctor)

    patient_data_serializer = PatientProfileSerializer(patient_data)
    patient_appointments_serializer = PatientAppointmentSerializer(patient_appointments, many=True)

    return Response(
        {
            "patient_data":patient_data_serializer.data,
            "patient_appointments":patient_appointments_serializer.data
        }
    )

# @api_view(['POST'])
# def register_doctor(request, format=None):
#     """"API endpoint for doctor Registration"""

#     userSerializer = UserCreateSerializer(data=request.data)

#     if userSerializer.is_valid():
#         user = userSerializer.save()

#         doctorSerializer = DoctorSerializer(data=request.data)
#         if doctorSerializer.is_valid():
#             doctorSerializer.save(user=user)

#             return Response({'message': "doctor and user created"}, status=status.HTTP_201_CREATED)
#         return Response({'message': doctorSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#     return Response({'message': userSerializer.errors}, status=status.HTTP_400_BAD_REQUEST) 