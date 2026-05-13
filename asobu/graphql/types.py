import strawberry
import strawberry_django
from strawberry import auto

from base.service import BaseService
from base.graphql.types import FranchiseType
from talent.graphql.types import CharacterType, VoiceActorType

from asobu.models import Game
from asobu.service import AsobuService

@strawberry.type
class GameCharacterType:
    character: CharacterType
    role: str
    voice_actor: VoiceActorType

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

    @strawberry_django.field
    def franchise(self) -> FranchiseType:
        return BaseService.franchise.get_franchise(self.franchise.id)
    
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
