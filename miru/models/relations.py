from django.db import models
from talent.models import Character

class RelatedAnime(models.Model):

    class Type(models.TextChoices):
        SPINOFF = 'spinoff', 'Spin-off'
        SIDE_STORY = 'side_story', 'Side Story'
        ALTERNATIVE_VERSION = 'alternative_version', 'Alternative Version'
        OTHER = 'other',  'Other'

    source_anime = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='children_anime')
    node_anime = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='parent_anime')
    relation_type = models.CharField(choices=Type.choices, default=Type.OTHER, blank=True)

class AnimeCharacter(models.Model):

    class Role(models.IntegerChoices):
        MAIN = 0, 'Main'
        SUPPORT = 1, 'Supporting'

    anime=models.ForeignKey('miru.anime', on_delete=models.CASCADE, related_name='cast')
    character=models.ForeignKey(Character, on_delete=models.CASCADE)
    role=models.IntegerField(choices=Role.choices, default=Role.SUPPORT, blank=True)

    class Meta:
        unique_together = ('anime', 'character')

    def __str__(self):
        return f"{self.character} in {self.anime} as {self.get_role_display()} character"
    
class AnimeEpisode(models.Model):

    number = models.IntegerField()
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(default='A description will be written later')
    anime = models.ForeignKey('miru.anime', on_delete=models.CASCADE, null=False, blank=False, related_name='episodes')
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['anime', 'number']
        
    def __str__(self):
        if self.title:
            return f"Ep: {self.number} - {self.title}"
        return f"Ep: {self.number}"

