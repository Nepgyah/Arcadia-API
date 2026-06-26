from django.db import models
from base.models import Review
from .anime import Anime

class AnimeReview(Review):

    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, db_index=True)

    class Meta:
        unique_together = ('profile_id', 'anime')

    def __str__(self):
        return f'User {self.profile_id} - Anime: {self.anime.id}'