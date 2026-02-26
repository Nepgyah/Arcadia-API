from django.db import models

from util.helpers import unique_slugify
from characters.models import Character

class Talent(models.Model):
    """
    Abstract model for real personalities that include voice actors, music artists, etc
    """

    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(default='A bio will be written later', blank=True)
    socials = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.display_name)
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        raise NotImplementedError
    
    def __str__(self):
        return self.display_name
    
class VoiceActor(Talent):
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150, null=True, blank=True)

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}"
    
class Artist(Talent):
    name = models.CharField(max_length=150)
    voice_actor = models.OneToOneField(VoiceActor, on_delete=models.SET_NULL, null=True, blank=True, related_name='artist_profile')
    character = models.OneToOneField(Character, on_delete=models.SET_NULL, null=True, blank=True, related_name='artist_profile')
    special_message = models.TextField(null=True, blank=True)

    @property
    def display_name(self):
        if self.voice_actor:
            return self.voice_actor.display_name
        if self.character:
            return self.character
        else:
            return self.name
