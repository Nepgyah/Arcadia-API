from django.db import models
from base.models import Company

class Organizer(Company):
    description = models.TextField(blank=True, default='A description will be written later')

class Event(models.Model):
    name = models.CharField(max_length=255)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
