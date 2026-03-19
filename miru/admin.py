import logging
from django.db import transaction, IntegrityError
from django.contrib import admin
from base.anilist_scripts.syncGenres import SyncGenres
from miru.anilist.syncAnimeCompanies import SyncAnimeCompanies
from miru.anilist.fetchAnilistData import FetchAnilistData
from miru.anilist.syncMainData import SyncMainData
from miru.anilist.syncEpisodes import SyncEpisodes
from miru.anilist.syncCharacters import SyncCharacters
from .models.anime import (
    Anime,
    AniListData
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

@admin.register(AniListData)
class AniListImporterAdmin(admin.ModelAdmin):
    form = AniListForm

    def save_model(self, request, obj, form, change):
        anilist_id = form.cleaned_data.get('anilist_id')

        try:
            with transaction.atomic():
                logging.basicConfig(level=logging.INFO)
                anime_obj = Anime()
                anilist_data = FetchAnilistData(anilist_id)
                logging.info("Fetching anilist data: Success - Anilist ID: %s", anilist_id)

                SyncMainData(anime_obj, anilist_data)
                anime_obj.save()
                logging.info("Saving anime object: Success - ID: %s", anime_obj.id)

                SyncAnimeCompanies(anime_obj, anilist_data)
                logging.info('Syncing companies: Success')

                genre_list = SyncGenres(anilist_data)
                anime_obj.genres.set(genre_list)
                logging.info('Syncing genres: Success')

                SyncEpisodes(anime_obj, anilist_data)
                logging.info('Syncing episodes: Success')

                SyncCharacters(anime_obj, anilist_data)
                logging.info('Syncing characters: Success')

                rank_score = None
                rank_popular = None

                for rank_item in anilist_data.get('rankings'):
                    if rank_item.get('type') == 'POPULAR' and bool(rank_item.get('allTime')):
                        rank_popular = rank_item.get('rank')
                    
                    if rank_item.get('type') == 'RATED' and bool(rank_item.get('allTime')):
                        rank_score = rank_item.get('rank')
                
                logging.info('Syncing anilist rankings: Success')

                obj.anime = anime_obj
                obj.anilist_id = anilist_id
                obj.rank_score = rank_score
                obj.rank_popular = rank_popular
                
                logging.basicConfig(level=logging.WARNING)

                return super().save_model(request, obj, form, change)
            
        except Exception as e:
            logging.error('Exception: %s', e)