from django.db import models
from account.models import User


CHOICES = (
        ('PN', 'Poniedziałek'),
        ('WT', 'Wtorek'),
        ('ŚR', 'Środa'),
        ('CZ', 'Czwartek'),
        ('PT', 'Piątek'),
    )


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=9)
    specialization = models.CharField(max_length=50)
    working_days = models.CharField(max_length=25, choices=CHOICES)
    

    @property
    def get_name(self):
        return self.first_name+" "+self.last_name
    
    def __str__(self):
        return self.first_name+" "+self.last_name
