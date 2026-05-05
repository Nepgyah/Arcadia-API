from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from asobu.models import Game
from users.models import ArcadiaUser

class GameListEntry(models.Model):
        
    class StatusType(models.IntegerChoices):
        PLAYING = 0, 'Playing'
        COMPLETED = 1, 'Completed'
        PLAN_TO = 2, 'Plan To Play'
        ON_HOLD = 3, 'On Hold'
        REPLAYING = 4, 'Replaying'
    
    user = models.ForeignKey(ArcadiaUser, on_delete=models.CASCADE, related_name='game_list')
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
    review = models.TextField(null=True, blank=True)
    review_update_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True, blank=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['status']),
        ]
        unique_together = ['user', 'game']

    def __str__(self):
        return f'User: {self.user.username} - Game: {self.game.title} - Status: {self.get_status_display()}'