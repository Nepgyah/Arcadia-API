from django.db import models
from base.models import (
    Genre,
    Media
)
from talent.models import Character
from .misc import AnimeCompany
from miru.anilist.anilist_main import FetchAnilistEntry

class Anime(Media):
    
    class Meta:
        ordering = ['title']
    
    class MediaType(models.IntegerChoices):
        TV = 0, 'Tv'
        MOVIE = 1, 'Movie'
        OVA = 2, 'Ova'
        ONA = 3, 'Ona'
        WEB = 4, 'Web'

    class Status(models.IntegerChoices):
        NOT_YET_AIRED = 0, 'Not yet aired'
        AIRING = 1, 'Airing'
        FINISHED_AIRING = 2, 'Finished airing'
        DELAYED = 3, 'Delayed'
        CANCELLED = 4, 'Cancelled'

    class Season(models.IntegerChoices):
        WINTER = 0, 'Winter'
        SPRING = 1, 'Spring'
        SUMMER = 2, 'Summer'
        FALL = 3, 'Fall'

    class Rating(models.IntegerChoices):
        NOT_RATED = 0, 'Not yet rated'
        G = 1, 'All ages'
        PG = 2, 'Children'
        PG_13 = 3, 'Teens 13 or older'
        R = 4, '17+ (Violence/Profanity)'

    title_native = models.CharField(max_length=255, null=True, blank=True, help_text='The origin way to write the anime')
    title_romaji = models.CharField(max_length=255, null=True, blank=True, help_text='How to pronounce the name with the english alphabet')
    other_titles = models.JSONField(default=[], null=True, blank=True, help_text='Ways to call the anime part from Japanese and English')
    season = models.IntegerField(choices=Season.choices, default=None, null=True, blank=True)
    season_year = models.SmallIntegerField(null=True, blank=True)
    type = models.IntegerField(choices=MediaType, default=MediaType.TV)
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_YET_AIRED, blank=True)
    rating = models.IntegerField(choices=Rating.choices, default=Rating.NOT_RATED)
    genres = models.ManyToManyField(Genre, related_name='animes', blank=True)
    episode_count = models.SmallIntegerField(null=True, blank=True)
    hashtag = models.CharField(max_length=128, null=True, blank=True)
    banner_img_url = models.URLField(null=True, blank=True)
    cover_img_url = models.URLField(null=True, blank=True)

    characters = models.ManyToManyField(Character, through='AnimeCharacter', related_name='animes', blank=True)

    producer = models.ManyToManyField(AnimeCompany, related_name='produced_animes', null=True, blank=True)
    studio = models.ManyToManyField(AnimeCompany, related_name='studio_animes', null=True, blank=True)

    prev_anime = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_entries')
    related_anime = models.ManyToManyField('self', through='RelatedAnime', symmetrical=False, related_name='related_to_anime', blank=True)

    airing_start_date=models.DateField(null=True, blank=True)
    airing_end_date=models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
    
    @property
    def season_string(self):
        if self.season is None and self.season_year is None:
            return None
        return f"{self.get_season_display()} {self.season_year}"
    
class AniListData(models.Model):

    anime = models.OneToOneField(Anime, on_delete=models.CASCADE, null=True, blank=True)
    anilist_id = models.IntegerField(null=False, blank=False)
    rank_score = models.SmallIntegerField(null=True, blank=True)
    rank_popular = models.SmallIntegerField(null=True, blank=True)

class AniListImporter(AniListData):
    class Meta:
        proxy = True
        verbose_name = "Anilist Importer"
        verbose_name_plural = "Anilist Importers"

    def sync_with_anilist(self):
        FetchAnilistEntry(self)