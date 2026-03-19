from django.db import transaction, IntegrityError
from django.contrib import admin
from base.anilist_scripts.syncGenres import SyncGenres
from miru.anilist.fetchAnilistData import FetchAnilistData
from miru.anilist.syncMainData import SyncMainData
from miru.anilist.syncEpisodes import SyncEpisodes
from miru.anilist.syncCharacters import SyncCharacters
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
        anilist_id = form.cleaned_data.get('anilist_id')

        #TODO: Call anilist data script
        try:
            with transaction.atomic():
                anime_obj = Anime()
                anilist_data = FetchAnilistData(anilist_id)
                SyncMainData(anime_obj, anilist_data)

                #TODO: SAVE ANIME OBJ
                anime_obj.save()
                
                genre_list = SyncGenres(anilist_data)
                anime_obj.genres.set(genre_list)
                
                SyncEpisodes(anime_obj, anilist_data)

                SyncCharacters(anime_obj, anilist_data)


        except Exception as e:
            print(f'integrity error: {e}')
        # obj.sync_with_anilist()
        # return super().save_model(request, obj, form, change)