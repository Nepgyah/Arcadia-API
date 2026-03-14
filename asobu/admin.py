from django.contrib import admin
from .models import (
    Developer,
    Platform,
    Publisher,
    Tag,
    Game,
    DLC,
    GamePlatform,
    GameRelation,
    GameCharacter
)

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    search_fields = ['name']

class GameCharacterInline(admin.TabularInline):
    model = GameCharacter
    extra = 1
    autocomplete_fields = ['character']

class GameRelationInline(admin.TabularInline):
    model = GameRelation
    fk_name = 'to_game'
    extra = 1
    autocomplete_fields = ['from_game']

class GamePlatformInline(admin.TabularInline):
    model = GamePlatform
    extra = 1
    autocomplete_fields = ['platform']

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [GameCharacterInline, GameRelationInline, GamePlatformInline]
    search_fields = ['title']
    
admin.site.register(Tag)
admin.site.register(DLC)

