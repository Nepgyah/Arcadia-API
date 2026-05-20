from django.db import models
from django.contrib.auth.models import User

class ArcadiaProfile(models.Model):
    d2x_id = models.IntegerField(unique=True, null=True, blank=True)
    admin_account = models.OneToOneField(User, on_delete=models.SET_NULL, name=True, blank=True)
    username = models.CharField(max_length=50)
    picture_preset = models.IntegerField(default=0, null=True, blank=True)

    @property
    def is_admin(self):
        return True if self.admin_account is not None else False