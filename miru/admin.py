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
from miru.anilist.anilist_main import FetchAnilistEntry

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
        anime_obj = Anime()
        FetchAnilistEntry(anime_obj)
        print('Done')
        print(anime_obj.title)
        print(anime_obj.airing_start_date)
        print(anime_obj.airing_end_date)
        # obj.sync_with_anilist()
        # return super().save_model(request, obj, form, change)