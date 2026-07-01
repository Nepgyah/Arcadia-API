from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from base.models import Franchise
from .util import unique_slugify

class SlugMixin(models.Model):
    slug=models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = unique_slugify(instance=self, value=self.name)
        super().save(*args, **kwargs)

class ImageMixin(models.Model):
    cover_image_url = models.URLField(null=True, blank=True)
    banner_image_url = models.URLField(null=True, blank=True)
    bg_image_url = models.URLField(null=True, blank=True)

    class Meta:
        abstract = True

class TimestampMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class PublicMixin(models.Model):
    is_public = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def set_status(self, status: bool) -> None:
        self.is_public = status
        self.save()

class ProfileIDMixin(models.Model):
    profile_id = models.IntegerField(null=False, blank=False, db_index=True)

    class Meta:
        abstract = True

class CompanyMixin(
    SlugMixin,
    models.Model
):
    name=models.CharField(max_length=150, null=False, blank=False)
    
    class Meta:
        abstract = True

class ReviewMixin(
    TimestampMixin,
    ProfileIDMixin,
    models.Model
):
    score = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        db_index=True
    )
    text = models.TextField(default="A review will be written later")
    like_count = models.IntegerField(blank=True, default=0)
    dislike_count = models.IntegerField(blank=True, default=0)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class MediaMixin(
    ImageMixin,
    TimestampMixin,
    SlugMixin,
    models.Model
):
    title = models.CharField(max_length=255)
    score = models.FloatField(default=0.0)
    users = models.IntegerField(default=0)
    franchise=models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True)
    summary=models.TextField(default='A synopsis will be written later.')

    class Meta:
        abstract = True