from django.db import models
from .anime import Anime

class FavoriteAnime(models.Model):

    profile_id = models.IntegerField(null=False, blank=False, db_index=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        unique_together = ['profile_id', 'anime']