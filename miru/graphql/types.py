import strawberry
import strawberry_django
from typing import Optional
from base.graphql.types import FranchiseType, GenreType
from talent.graphql.types import CharacterType, VoiceActorType

from miru.models import Anime, AnimeCompany, AnimeListEntry, MyAnimeListData, AnimeCharacter, AniListData, AnimeEpisode
from miru.service import MiruService
from miru.repository import MiruRepository

@strawberry_django.type(
    AnimeListEntry,
    fields="__all__"
)
class AnimeListEntryType:
    anime: "AnimeType"

@strawberry_django.type(
    MyAnimeListData,
    fields="__all__"
)
class MALDataType:
    pass

@strawberry_django.type(
    AniListData,
    fields="__all__"
)
class AnilistDataType:
    pass

@strawberry_django.type(
    AnimeCompany,
    fields="__all__"
)
class AnimeCompanyType:
    pass

@strawberry_django.type(
    AnimeEpisode,
    fields="__all__"
)
class EpisodeType:
    pass

@strawberry.type()
class AnimeCharacterType:
    """
        Custom type based of of animecharacter model, 
        raises the voice actor to top level instead of underneath character
    """

    character: CharacterType
    role: str
    voice_actor: VoiceActorType | None

@strawberry_django.type(
    Anime, 
    exclude=['characters', 'prev_anime', 'related_anime', 'type', 'status', 'season', 'rating'],
    description="Animation media for the Miru app"
)
class AnimeType:
    franchise : FranchiseType | None
    studio: list[AnimeCompanyType]
    producer: list[AnimeCompanyType]
    prequel: Optional["AnimeType"] = strawberry_django.field(field_name="prev_anime")

    @strawberry_django.field
    def cast(self) -> list[AnimeCharacterType]:
        characters = MiruService.anime.get_cast(self.id)
        return [
            AnimeCharacterType(
                character=character['character'],
                role=character['role'],
                voice_actor=character['voice_actor']
            )
            for character in characters
        ]
    
    @strawberry_django.field
    def status(self) -> str:
        return self.get_status_display()
    
    @strawberry_django.field
    def type(self) -> str:
        return self.get_type_display()
    
    @strawberry_django.field
    def rating(self) -> str:
        return self.get_rating_display()
    
    @strawberry_django.field
    def season(self) -> str:
        return self.season_string
    
    @strawberry_django.field
    def bg_url(self) -> str | None:
        return self.bg_url
    
    @strawberry_django.field
    def genres(self) -> list[GenreType]:
        return self.genres.all()

    @strawberry_django.field
    def sequels(self) -> list["AnimeType"]:
        return self.next_entries.all()
    
    @strawberry_django.field
    def mal_data(self) -> MALDataType | None:
        try:
            return MiruRepository.anime.get_mal_data(self.id)
        except:
            return None
    
    @strawberry_django.field
    def anilist_data(self) -> AnilistDataType | None:
        try:
            return MiruRepository.anime.get_anilist_data(self.id)
        except:
            return None
        
    @strawberry_django.field
    def episodes(self) -> list[EpisodeType]:
        return MiruRepository.anime.get_episodes(self.id)
        
@strawberry.type
class AppearanceType:
    role: str
    anime: AnimeType
    
@strawberry.type
class CharacterAppearanceType:
    character: CharacterType
    appearances: list[AppearanceType]