from django.db import models
from util.helpers import unique_slugify

# Create your models here.
class Character(models.Model):
    first_name=models.CharField(max_length=150, blank=False)
    last_name=models.CharField(max_length=150, null=True, blank=True)
    nicknames=models.JSONField(default=list, blank=True)
    slug=models.SlugField(unique=True, blank=True)
    # played_by=models.ForeignKey(VoiceActor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            full_name = f"{self.first_name} {self.last_name}".strip()
            self.slug = unique_slugify(self, full_name)
        super().save(*args, **kwargs)