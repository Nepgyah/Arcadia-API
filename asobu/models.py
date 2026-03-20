from django.db import models

from base.models import Company, Media, Genre
from talent.models import Character
from util.helpers import unique_slugify

class GameCompany(Company):

    def __str__(self):
        return f"{self.name}"
    
class Platform(models.Model):

    name=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"
    
    
class Tag(models.Model):

    name=models.CharField(max_length=150)

    def __str__(self):
        return str(self.name)
    
class Game(Media):
    
    class Status(models.IntegerChoices):
        ANNOUNCED = 0, 'Announced'
        IN_PRODUCTION = 1, 'In Production'
        RELEASED = 2, 'Released'
        EOS = 3, 'End of Service'
        CANCELLED = 4, 'Cancelled'

    class ESRB(models.IntegerChoices):
        EVERYONE = 0, 'Everyone'
        EVERYONE_10 = 1, 'Everyone 10+'
        TEEN = 2, 'Teen'
        MATURE = 3, 'Mature 17+'
        ADULT = 4, 'Adults Only 18+'
        PENDING = 5, 'Rating Pending'
        PENDING_MATURE = 6, 'Rating Pending (Likely Mature)'
    
    class PEGI(models.IntegerChoices):
        PEGI_3 = 0, 'PEGI 3'
        PEGI_7 = 1, 'PEGI 7'
        PEGI_12 = 2, 'PEGI 12'
        PEGI_16 = 3, 'PEGI 16'
        PEGI_18 = 4, 'PEGI 18'
        PEGI_PENDING = 5, 'Rating Pending'

    status = models.IntegerField(choices=Status.choices, default=Status.ANNOUNCED)
    tags = models.ManyToManyField(Tag, related_name='tagged_games', blank=True)
    genres = models.ManyToManyField(Genre, related_name='games', blank=True)
    esrb_rating = models.IntegerField(choices=ESRB.choices, default=ESRB.PENDING)
    pegi_rating = models.IntegerField(choices=PEGI.choices, default=PEGI.PEGI_PENDING)
    prev_game = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_entries')
    trailer_url = models.URLField(null=True, blank=True)
    
    characters = models.ManyToManyField(Character, through='GameCharacter', related_name='games')
    platforms = models.ManyToManyField(Platform, through='GamePlatform', related_name='released_games')

    developers = models.ManyToManyField(GameCompany, related_name='developed_games', blank=True)
    publishers = models.ManyToManyField(GameCompany, related_name='published_games', blank=True)
    
    steam_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-score']

    def __str__(self):
        return str(self.title)

class DLC(models.Model):

    class DLCType(models.IntegerChoices):
        STORY = 0, 'Story'
        COSMETIC = 1, 'Cosmetic'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    score = models.FloatField(default=0.0)
    slug = models.SlugField(unique=True, blank=True)
    type = models.IntegerField(choices=DLCType.choices, default=DLCType.STORY, blank=True)

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(instance=self, value=self.title)
        super().save(*args, **kwargs)

class GamePlatform(models.Model):
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    release_date = models.DateField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game', 'platform'], name='unique_game_platform')
        ]
        ordering = ['release_date']

    def __str__(self):
        return f"{self.game.title} on {self.platform.name}"
    
class GameRelation(models.Model):
    """
        Misc relation case that is not a dlc or part of the main game progression.
        Example: Global release, etc
    """

    class Type(models.TextChoices):
        RE_RELEASE = 're_release', 'Re-release'
        OTHER = 'other', 'Other'

    from_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='as_predeccessor')
    to_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='as_sucessor')
    type = models.CharField(choices=Type.choices, default=Type.RE_RELEASE, blank=True)

    def __str__(self):
        return f"{self.to_game.title} is a {self.get_type_display()} for {self.from_game.title}"
    
class GameCharacter(models.Model):
    """A intermediate model for a character and a game"""
    
    class Role(models.IntegerChoices):
        MAIN = 0, 'Main'
        SUPPORTING = 1, 'Supporting'

    game = models.ForeignKey(Game, null=False, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, null=False, on_delete=models.CASCADE)
    is_playable = models.BooleanField(default=False)
    role = models.IntegerField(choices=Role.choices, default=Role.SUPPORTING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game', 'character'], name='unique_game_character')
        ]
        indexes = [
            models.Index(fields=['game'])
        ]

    def __str__(self):
        return f"{self.character} in {self.game} as {self.get_role_display()} character"