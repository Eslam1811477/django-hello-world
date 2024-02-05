from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    national_ID = models.BigIntegerField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mother_phone_number = models.CharField(max_length=20, null=True, blank=True)
    father_phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name
