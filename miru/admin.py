import logging
from django.db import transaction
from django.contrib import admin, messages
from base.anilist_scripts.syncGenres import SyncGenres
from miru.myanimelist.syncRankings import syncMALRankings
from miru.anilist import (
    fetch_anilist_data,
    sync_characters,
    sync_companies,
    sync_episodes,
    sync_metadata
)
from .models.anime import (
    Anime,
    AniListData,
    MyAnimeListData
)
from .models.relations import (
    AnimeCharacter,
    AnimeEpisode,
    RelatedAnime
)
from .forms import AniListForm
from .models.misc import AnimeCompany
from .models.list import AnimeListEntry

logger = logging.getLogger(__name__)

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

@admin.register(MyAnimeListData)
class MyAnimeListAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        mal_id = form.cleaned_data.get('mal_id')
        try:
            rank_by_score, rank_by_popularity = syncMALRankings(mal_id)
            obj.rank_score = rank_by_score
            obj.rank_popular = rank_by_popularity
            super().save_model(request, obj, form, change)
            self.message_user(request, "MyAnimeList data successfully updated.", messages.SUCCESS)

        except Exception as e:
            logging.error("MAL Admin Import Failed: %s", e) 
            self.message_user(request, f"Import Failed: {str(e)}", messages.ERROR)

        
@admin.register(AniListData)
class AniListImporterAdmin(admin.ModelAdmin):
    form = AniListForm

    def save_model(self, request, obj, form, change):
        anilist_id = form.cleaned_data.get('anilist_id')
        print('Check one')
        try:
            with transaction.atomic():
                anime_obj = Anime()
                anilist_data = fetch_anilist_data(anilist_id)
                logger.info("Fetching anilist data: Success - Anilist ID: %s", anilist_id)

                sync_metadata(anime_obj, anilist_data)
                anime_obj.save()
                logger.info("Saving anime object: Success - ID: %s", anime_obj.id)
                sync_companies(anime_obj, anilist_data)
                logger.info('Syncing companies: Success')

                genre_list = SyncGenres(anilist_data)
                anime_obj.genres.set(genre_list)
                logger.info('Syncing genres: Success')
                sync_episodes(anime_obj, anilist_data)
                logger.info('Syncing episodes: Success')
                sync_characters(anime_obj, anilist_data)
                logger.info('Syncing characters: Success')
                rank_score = None
                rank_popular = None

                for rank_item in anilist_data.get('rankings'):
                    if rank_item.get('type') == 'POPULAR' and bool(rank_item.get('allTime')):
                        rank_popular = rank_item.get('rank')
                    
                    if rank_item.get('type') == 'RATED' and bool(rank_item.get('allTime')):
                        rank_score = rank_item.get('rank')
                
                logger.info('Syncing anilist rankings: Success')
                obj.anime = anime_obj
                obj.anilist_id = anilist_id
                obj.rank_score = rank_score
                obj.rank_popular = rank_popular

                return super().save_model(request, obj, form, change)
            
        except Exception as e:
            print(e)
            logger.error(e)