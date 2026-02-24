from miru.models import (
    Anime,
    AnimeCharacter
)

class MiruRepository:
    ''' Repository layer to work with Anime, AnimeCharacters, etc '''

    @staticmethod
    def get_anime_by_id(id):
        try:
            return Anime.objects.get(id=id)
        except Anime.DoesNotExist:
            return None
        
    @staticmethod
    def get_characters_by_anime(id):
        """
            Returns a list of characters related to an anime.

            Return None if no characters found
        """

        try:
            anime = Anime.objects.get(id=id)
            return AnimeCharacter.objects.filter(anime=anime)
        except Anime.DoesNotExist:
            return []
        
    @staticmethod
    def get_anime_by_category(category, count):
        return Anime.objects.order_by(category)[:5]