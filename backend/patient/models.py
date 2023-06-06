from django.db import models
from account.models import User
from doctor.models import Doctor 


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pesel = models.CharField(max_length=11)
    phone_number = models.CharField(max_length=9)

    @property
    def get_name(self):
        return self.first_name+" "+self.last_name
    
    def __str__(self):
        return self.first_name+" "+self.last_name


class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    prescription = models.TextField(blank=True)
    status = models.BooleanField(default=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    @property
    def patient_name(self):
        self.patient.get_name
    
    def __str__(self):
        return self.patient.get_name+'-'+self.doctor.get_name + " " + str(self.date)