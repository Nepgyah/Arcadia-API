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

class GameCharacterInline(admin.TabularInline):
    model = GameCharacter
    extra = 1
    autocomplete_fields = ['character']

class GameRelationInline(admin.TabularInline):
    model = GameRelation
    extra = 1,
    autocomplete_fields = ['from_game']

class GamePlatformInline(admin.TabularInline):
    model = GamePlatform
    extra = 1
    autocomplete_fields = ['platform']

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [GameCharacterInline, GameRelation]
    search_fields = ['title']
    
admin.site.register(Developer)
admin.site.register(Platform)
admin.site.register(Publisher)
admin.site.register(Tag)
admin.site.register(DLC)

