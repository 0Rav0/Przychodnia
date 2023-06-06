from rest_framework import serializers
from django.contrib.auth.models import Group

from account.models import User
from doctor.models import Doctor
from patient.models import Patient, Appointment


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

        group_patient, created = Group.objects.get_or_create(name='patient')
        group_patient.user_set.add(user)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        password = validated_data.get("password")

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'pesel', 'phone_number')


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    # doctor = serializers.StringRelatedField()
    doctor = serializers.PrimaryKeyRelatedField(many=False, queryset=Doctor.objects.all())
    
    prescription = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ( 'id', 'date','time', 'patient', 'doctor', 'status', 'reason', 'prescription')


class AppointmentListSerializer(serializers.ModelSerializer):
    # patient = serializers.StringRelatedField()
    doctor = serializers.StringRelatedField()
    
    prescription = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ( 'id', 'date','time', 'doctor', 'status', 'reason', 'prescription')
    

# class PatientCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Patient
#         fields = 
    # first_name = serializers.CharField(required=False)
    # last_name = serializers.CharField(required=False)
    # pesel = serializers.CharField(required=False)
    # phone = serializers.CharField(required=False)


    # def validate_phone(self, phone):
    #     if phone.isdigit()==False:
    #         raise serializers.ValidationError('Please Enter a valid phone number!')
    #     return phone
    
    # def create(self, validated_data):
    #     new_patient = Patient.objects.create(user = validated_data['user'])
    #     return new_patient
    
    # def update(self, instance, validated_data):
    #     # instance.phone=validated_data.get('phone', instance.phone)
    #     instance.save()

    #     return instance