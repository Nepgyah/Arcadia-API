from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from arcadia.mixins import ProfileIDMixin, ReviewMixin, TimestampMixin
from asobu.models import Game

class GameListEntry(ProfileIDMixin, TimestampMixin, models.Model):
        
    class StatusType(models.IntegerChoices):
        PLAYING = 0, 'Playing'
        COMPLETED = 1, 'Completed'
        PLAN_TO = 2, 'Plan To Play'
        ON_HOLD = 3, 'On Hold'
        REPLAYING = 4, 'Replaying'

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.IntegerField(choices=StatusType, default=StatusType.PLAYING)
    score = models.SmallIntegerField(
        blank=True, 
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    note = models.CharField(null=True, blank=True, max_length=256)
    start_play_date = models.DateField(null=True, blank=True)
    end_play_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['status']),
        ]
        unique_together = ['profile_id', 'game']

    def __str__(self):
        return f'User: {self.user.username} - Game: {self.game.title} - Status: {self.get_status_display()}'
    
class Review(ReviewMixin, models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['profile_id', 'game']