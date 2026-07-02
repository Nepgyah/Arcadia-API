from django.db import models
from arcadia.mixins import CompanyMixin

class GameCompany(CompanyMixin):

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