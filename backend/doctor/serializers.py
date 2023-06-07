from rest_framework import serializers
from django.contrib.auth.models import Group

from patient.models import Appointment
from account.models import User
from doctor.models import Doctor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

    def validate_email(self, email):
        email_exists=User.objects.filter(email=email).first()
        if email_exists:
            raise serializers.ValidationError({'email':'This email already exists'})
        return email


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = "__all__"
    
    def validate_email(self, email):
        email_exists=User.objects.filter(email=email).first()
        if email_exists:
            raise serializers.ValidationError({'email':'This email already exists'})
        return email

    # def validate_password(self, password):
    #     if password.isdigit():
    #         raise serializers.ValidationError('Your password should contain letters!')
    #     return password  


    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        group_doctor, created = Group.objects.get_or_create(name='doctor')
        group_doctor.user_set.add(user)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        password = validated_data.get("password")

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class DoctorSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()

    class Meta:
        model = Doctor
        fields = ('user', 'first_name', 'last_name', 'specialization',)


class DoctorDetailSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    working_days = serializers.SlugRelatedField(many=True, read_only=True, slug_field='day'  )
    working_hours = serializers.SlugRelatedField(many=True, read_only=True, slug_field='time' )

    class Meta:
        model = Doctor
        exclude = ('id',)


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    doctor = serializers.StringRelatedField()
    
    reason = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    time = serializers.TimeField(read_only=True)
    room = serializers.IntegerField(read_only=True)

    class Meta:
        model = Appointment
        fields = ( 'id', 'date', 'time', 'patient', 'doctor', 'status', 'reason', 'prescription', 'recommendations', 'room')

    def update(self, instance, validated_data):
        instance.status = 2
        return super().update(instance, validated_data)


class PatientAppointmentSerializer(serializers.ModelSerializer):
    reason = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    time = serializers.TimeField(read_only=True)
    room = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Appointment
        fields = ( 'id','date', 'time', 'status', 'reason', 'prescription', 'recommendations')
