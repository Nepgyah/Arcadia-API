from django.db import models

# Create your models here.
class User(models.Model):
    '''
        Pseudo user class, serves as a in between for 
        arcadia account related models and main d2x accounts.
    '''

    d2x_id = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"D2X User ID: {self.id}"
    
    @property
    def is_authenticated(self):
        return True