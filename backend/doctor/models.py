from django.db import models
from account.models import User


class Day(models.Model):
    day = models.CharField(max_length=20)
    short = models.CharField(max_length=3, )

    def __str__(self):
        return self.day + "(" + self.short + ")"

class Hour(models.Model):
    time = models.TimeField()

    def __str__(self):
        return str(self.time)
        

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=9)
    specialization = models.CharField(max_length=50)
    working_days = models.ManyToManyField(Day, blank=True)
    working_hours = models.ManyToManyField(Hour, blank=True)

    @property
    def get_name(self):
        return self.first_name+" "+self.last_name
    
    def __str__(self):
        return self.get_name
