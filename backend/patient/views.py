from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from account.utils import Util
from account.models import User

from .models import Patient, Appointment
from .serializers import *

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='patient').exists())
        

@api_view(['POST'])
def register_patient(request, format=None):
    userSerializer = UserCreateSerializer(data=request.data)

    if userSerializer.is_valid():
        user = userSerializer.save()

        data = request.data.copy()
        data['user'] = user

        patientSerializer = PatientSerializer(data=data)

        if patientSerializer.is_valid():
            patientSerializer.save(user=user)

            # token = RefreshToken.for_user(user).access_token

            # current_site=get_current_site(request).domain
            # relativeLink = reverse('email_verify')
            # absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            # email_body = 'Hi '+user.email+' Use link below to verify your email \n'+absurl

            # data={
            #     'email_body':email_body, 
            #     'to_email': user.email,
            #     'email_subject':'Verify your email'}
            # Util.send_email(data)

            return Response({'message': "account created"}, status=status.HTTP_201_CREATED)
        return Response({'message': patientSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': userSerializer.errors}, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsPatient])
def patient_profile(request, format=None):
    if request.method == 'GET':
        user = request.user
        profile = Patient.objects.get(user=user)
        userSerializer=UserSerializer(user)
        profileSerializer = PatientProfileSerializer(profile)
        return Response({
            'user_data':userSerializer.data,
            'profile_data':profileSerializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        user = request.user
        profile = Patient.objects.get(user=user)
        profileSerializer = PatientProfileSerializer(instance=profile, data=request.data.get('profile_data'))
        
        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({'profile_data':profileSerializer.data}, status=status.HTTP_200_OK)
        return Response({'profile_data':profileSerializer.errors }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        user = request.user
        profile = Patient.objects.get(user=user)
        profileSerializer = PatientProfileSerializer(instance=profile, data=request.data.get('profile_data'), partial=True)

        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({'profile_data':profileSerializer.data }, status=status.HTTP_200_OK)
        return Response({'profile_data':profileSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AppointementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPatient]
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update' or self.action == 'update':
            return AppointmentSerializer
        else:
            return AppointmentListSerializer
    
    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        appointments = Appointment.objects.filter(patient=patient)
        return appointments   

    def perform_create(self, serializer):
        patient = Patient.objects.get(user=self.request.user)
        serializer.save(patient=patient, room=patient.id)  


@api_view(['GET'])
@permission_classes([IsPatient])
def appointment_status(request, status):
    user = request.user
    patient = Patient.objects.get(user=user)

    appointment = Appointment.objects.filter(patient=patient, status=status)
    appointmentSerializer = AppointmentSerializer(appointment, many=True)

    return Response(appointmentSerializer.data)


@api_view(['GET'])
@permission_classes([IsPatient])
def prescription_list(request):
    user = request.user
    patient = Patient.objects.get(user=user)

    appointment = Appointment.objects.filter(patient=patient)
    appointmentSerializer = PrescriptionSerializer(appointment, many=True)

    return Response(appointmentSerializer.data)


@api_view(['GET'])
@permission_classes([IsPatient])
def prescription_detail(request, pk):
    user = request.user
    patient = Patient.objects.get(user=user)

    appointment = Appointment.objects.get(pk=pk, patient=patient)
    appointmentSerializer = PrescriptionSerializer(appointment)

    return Response(appointmentSerializer.data)


@api_view(['GET'])
def email_verify(request):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])

        if not user.is_active:
            user.is_active = True
            user.save()

            return Response({"message": "email activated !!"}, status=status.HTTP_200_OK, )
        return Response({"message": ":)"}, status=status.HTTP_200_OK, )

    except jwt.ExpiredSignatureError as identifier:
        return Response({"message": "link expired"}, status=status.HTTP_400_BAD_REQUEST, )
    except jwt.exceptions.DecodeError as identifier:
        return Response({"message": str(identifier)}, status=status.HTTP_400_BAD_REQUEST, )