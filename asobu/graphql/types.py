from typing import Optional
import strawberry
import strawberry_django
from strawberry import auto

from base.service import FranchiseService, GenreService
from base.graphql.types import FranchiseType, GenreType
from talent.graphql.types import CharacterType, VoiceActorType

from asobu.models import Game, DLC, Tag, Platform, GameCompany, GamePlatform, GameListEntry, Review
from asobu.service import AsobuService
from asobu.repository import AsobuRepository

@strawberry_django.type(GameCompany, fields="__all__")
class GameCompanyType:
    pass

@strawberry_django.type(Tag, fields="__all__")
class TagType:
    pass

@strawberry_django.type(Platform, fields="__all__")
class PlatformType:
    pass

@strawberry.type
class PlatformReleaseType:
    platform: PlatformType
    release_date: str

@strawberry.type
class GameCharacterType:
    character: CharacterType
    role: str
    voice_actor: VoiceActorType

@strawberry_django.type(DLC, fields="__all__", description="Add on content to a video game")
class DLCType:
    pass

@strawberry_django.type(Review, fields="__all__")
class GameReviewType:
    pass

@strawberry_django.type(Game, description="Video games from the asobu app")
class GameType:
    id: auto
    title: auto
    score: auto
    users: auto
    slug: auto
    created_at: auto
    updated_at: auto
    bg_image_path: auto
    status: strawberry.auto
    prev_game: Optional['GameType']
    tags: list[TagType]
    developers: list[GameCompanyType]
    publishers: list[GameCompanyType]

    @strawberry_django.field
    def esrb_rating(self) -> str:
        return self.get_esrb_rating_display()
    
    @strawberry_django.field
    def pegi_rating(self) -> str:
        return self.get_pegi_rating_display()
    
    @strawberry_django.field
    def genres(self) -> list[GenreType]:
        return self.genres.all()

    @strawberry_django.field
    def franchise(self) -> FranchiseType:
        return FranchiseService.get_franchise(self.franchise.id)
    
    @strawberry_django.field
    def cast(self) -> list[GameCharacterType]:
        characters = AsobuService.game.get_cast(self.id)
        return [
            GameCharacterType(
                character=character['character'],
                role=character['role'],
                voice_actor=character['voice_actor']
            )
            for character in characters
        ]

    @strawberry_django.field
    def dlc(self) -> list[DLCType]:
        return AsobuService.game.get_dlc(self.id)
    
    @strawberry_django.field
    def release(self) -> list[PlatformReleaseType]:
        platform_releases = GamePlatform.objects.filter(game=self)
        return [
            PlatformReleaseType(
                platform=entry.platform,
                release_date=entry.release_date
            )
            for entry in platform_releases
        ]
    
    @strawberry_django.field
    def reviews(self) -> list[GameReviewType]:
        return AsobuRepository.game.get_reviews(self.id)
    
@strawberry_django.type(GameListEntry, fields="__all__")
class GameListEntryType:
    game: GameType