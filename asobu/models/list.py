from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from asobu.models import Game

class GameListEntry(models.Model):
        
    class StatusType(models.IntegerChoices):
        PLAYING = 0, 'Playing'
        COMPLETED = 1, 'Completed'
        PLAN_TO = 2, 'Plan To Play'
        ON_HOLD = 3, 'On Hold'
        REPLAYING = 4, 'Replaying'
    
    profile_id = models.IntegerField(null=False, blank=False, db_index=True)
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
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['status']),
        ]
        unique_together = ['profile_id', 'game']

    def __str__(self):
        return f'User: {self.user.username} - Game: {self.game.title} - Status: {self.get_status_display()}'
    
class Review(models.Model):

    profile_id = models.IntegerField(null=False, blank=False, db_index=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    funny_count = models.PositiveIntegerField(default=0, blank=True)
    helpful_count = models.PositiveIntegerField(default=0, blank=True)
    nice_count = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        unique_together = ['profile_id', 'game']