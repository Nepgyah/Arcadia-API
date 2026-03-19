from django.contrib import admin
from .models import (
    VoiceActor,
    Artist,
    Character
)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']

@admin.register(VoiceActor)
class VoiceActorAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']

admin.site.register(Artist)