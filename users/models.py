from django.db import models
from django.contrib.auth.models import User

class ArcadiaUser(models.Model):
    d2x_id = models.IntegerField(unique=True, null=True, blank=True)
    admin_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=50)
    tag = models.IntegerField(null=True, blank=True)
    picture_preset = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.username}#{self.tag}' if self.tag else self.username
