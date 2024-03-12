from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    zone = models.CharField(max_length=20)
    budget = models.IntegerField()


    def __str__(self):
        return self.name
