import os
from dotenv import load_dotenv
from django.db import models
from util import unique_slugify

load_dotenv()

class Company(models.Model):
    name=models.CharField(max_length=150, null=False, blank=False)
    slug=models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        self.slug = unique_slugify(instance=self, value=self.name)
        super().save(*args, **kwargs)

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
    
class Media(models.Model):
    """
    Used as the base for Miru, Yomu, and Asobu
    """

    title = models.CharField(max_length=255)
    score = models.FloatField(default=0.0)
    users = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)
    summary=models.TextField(default='A synopsis will be written later.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    franchise=models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True)
    cover_image_url = models.URLField(null=True, blank=True)
    banner_image_url = models.URLField(null=True, blank=True)
    bg_image_url = models.URLField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-score']
    
    @property
    def bg_url(self):
        if self.bg_image_path is not None:
            return f'{os.environ.get('BG_CDN_BASE')}/{self.bg_image_path}'
        return None
    
    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = unique_slugify(instance=self, value=self.title)
        super().save(*args, **kwargs)
