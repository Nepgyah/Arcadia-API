from django.contrib import admin
from .models import (
    VoiceActor,
    Artist,
    Character
)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
admin.site.register(VoiceActor)
admin.site.register(Artist)