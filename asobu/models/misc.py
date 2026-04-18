from django.db import models
from base.models import Company

class GameCompany(Company):

    def __str__(self):
        return f"{self.name}"
    
class Platform(models.Model):

    name=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"
    
    
class Tag(models.Model):

    name=models.CharField(max_length=150)

    def __str__(self):
        return str(self.name)