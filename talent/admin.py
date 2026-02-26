from django.contrib import admin
from .models import (
    VoiceActor,
    Artist
)

admin.site.register(VoiceActor)
admin.site.register(Artist)