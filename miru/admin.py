from django.contrib import admin
from .models.anime import (
    Anime,
    AniListImporter
)
from .models.relations import (
    AnimeCharacter,
    AnimeEpisode,
    RelatedAnime
)
from .forms import AniListForm
from .models.misc import AnimeCompany
from .models.list_entry import AnimeListEntry

# Register your models here.
class AnimeCharacterInline(admin.TabularInline):
    model = AnimeCharacter
    extra = 1
    autocomplete_fields = ['character']

class RelatedAnimeInline(admin.TabularInline):
    model = RelatedAnime
    fk_name = 'source_anime'
    extra = 1
    autocomplete_fields = ['node_anime']

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    inlines = [AnimeCharacterInline, RelatedAnimeInline]
    search_fields = ['title']

admin.site.register(AnimeCompany)
admin.site.register(AnimeListEntry)
admin.site.register(AnimeEpisode)

@admin.register(AniListImporter)
class AniListImporterAdmin(admin.ModelAdmin):
    form = AniListForm

    def save_model(self, request, obj, form, change):

        #TODO: Call anilist data script
        print('Running Anilist')
        obj.sync_with_anilist()
        # return super().save_model(request, obj, form, change)