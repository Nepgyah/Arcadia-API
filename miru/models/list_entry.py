from django.db import models
from users.models import User
from .anime import Anime

class AnimeListEntry(models.Model):

    class StatusType(models.IntegerChoices):
        WATCHING = 0, 'Watching'
        COMPLETED = 1, 'Completed'
        PLAN_TO = 2, 'Plan To Watch'
        ON_HOLD = 3, 'On Hold'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.IntegerField(choices=StatusType, default=StatusType.WATCHING)
    current_episode = models.SmallIntegerField(default=0, blank=True)
    score = models.FloatField(null=True, blank=True)
    start_watch_date = models.DateField(null=True, blank=True)
    end_watch_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['anime']),
            models.Index(fields=['status']),
            models.Index(fields=["user", "status"]),
        ]
        unique_together = ('user', 'anime')

    def __str__(self):
        return f'{self.user} - Anime: {self.anime.title} - Status: {self.get_status_display()}'