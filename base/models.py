import os
from dotenv import load_dotenv
from django.db import models
from arcadia.util import unique_slugify

load_dotenv()

class Genre(models.Model):
    name=models.CharField(max_length=150)

    def __str__(self):
        return str(self.name)

class Franchise(models.Model):
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    socials = models.JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = unique_slugify(instance=self, value=self.name)
        super().save(*args, **kwargs)

    @property
    def cover_image_url(self):
        return f'{os.environ.get('BG_CDN_BASE')}/franchise/{self.id}/cover.jpg'
    
    @property
    def bg_image_url(self):
        return f'{os.environ.get('BG_CDN_BASE')}/franchise/{self.id}/bg.jpg'
