from django.db import models
from base.models import ArcadiaProfileMixin, TimestampMixin
from accounts.service import AccountsService
from .anime import Anime

class AnimeListEntry(models.Model):

    class StatusType(models.IntegerChoices):
        WATCHING = 0, 'Watching'
        COMPLETED = 1, 'Completed'
        PLAN_TO = 2, 'Plan To Watch'
        ON_HOLD = 3, 'On Hold'

    profile_id = models.IntegerField(null=False, blank=False, db_index=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.IntegerField(choices=StatusType, default=StatusType.WATCHING)
    note = models.CharField(null=True, blank=True, max_length=256)
    current_episode = models.SmallIntegerField(default=0, blank=True)
    start_watch_date = models.DateField(null=True, blank=True)
    end_watch_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['anime']),
            models.Index(fields=['status']),
            models.Index(fields=["profile_id", "status"]),
        ]
        unique_together = ('profile_id', 'anime')

    def __str__(self):
        return f'Anime: {self.anime.title} - Status: {self.get_status_display()}'

class CustomAnimeList(ArcadiaProfileMixin, TimestampMixin):

    title = models.CharField(max_length=125, blank=True, null=False)
    anime = models.ManyToManyField(Anime, related_name="custom_list_appearance")

    def save(self, *args, **kwargs):
        if self.pk is None and not self.title:
            previously_created_count = self.__class__.objects.filter(profile_id=self.profile_id).count()
            profile = AccountsService.profile.get_profile(self.profile_id)
            self.title = f"{profile.username}'s custom list #{previously_created_count + 1}"
        
        super().save(*args, **kwargs)