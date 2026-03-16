import graphene
from graphene_django import DjangoObjectType
from asobu.models import (
    GameCompany,
    Platform,
    Tag,
    Game,
    GameCharacter,
    GamePlatform,
    GameRelation,
    DLC
)
from base.schema import GenreType
from talent.graphql.schema import CharacterType

class GameCompanyType(DjangoObjectType):

    class Meta:
        model = GameCompany
        fields = "__all__"

class PlatformType(DjangoObjectType):

    class Meta:
        model = Platform
        fields = "__all__"

class TagType(DjangoObjectType):

    class Meta:
        model = Tag
        fields = "__all__"

class GameCharacterType(DjangoObjectType):
    
    class Meta:
        model = GameCharacter
        fields = "__all__"

    game = graphene.Field(lambda: GameType)
    character = graphene.Field(CharacterType)
    role = graphene.String()

    def resolve_game(self, info):
        try:
            Game.objects.get(id=self.game.id)
        except Game.DoesNotExist:
            return None
    
    def resolve_character(self, info):
        try:
            return GameCharacter.objects.get(character_id=self.character.id, game_id=self.game.id).character
        except GameCharacter.DoesNotExist:
            return None
        
    def resolve_role(self, info):
        return self.get_role_display()

class GamePlatformType(DjangoObjectType):

    class Meta:
        model = GamePlatform
        fields = "__all__"

    game = graphene.Field(lambda: GameType)
    platform = graphene.Field(lambda: PlatformType)
    
    def resolve_game(self, info):
        return Game.objects.get(id=self.game.id)
    
    def resolve_platform(self, info):
        return Platform.objects.get(id=self.platform.id)

class GameType(DjangoObjectType):

    class Meta:
        model = Game
        fields = "__all__"

    status = graphene.String()
    tags = graphene.List(TagType)
    genres = graphene.List(GenreType)
    esrb_rating = graphene.String()
    pegi_rating = graphene.String()
    developers = graphene.List(GameCompanyType)
    publishers = graphene.List(GameCompanyType)
    character_relations = graphene.List(GameCharacterType)
    platforms = graphene.List(GamePlatformType)

    def resolve_status(self, info):
        return self.get_status_display()
    
    def resolve_tags(self, info):
        return self.tags.all()

    def resolve_genres(self, info):
        return self.genres.all()
    
    def resolve_esrb_rating(self, info):
        return self.get_esrb_rating_display()
    
    def resolve_pegi_rating(self, info):
        return self.get_pegi_rating_display()
    
    def resolve_developers(self, info):
        return self.developers.all()

    def resolve_publishers(self, info):
        return self.publishers.all()
    
    def resolve_character_relations(self, info):
        return self.gamecharacter_set.all()
    
    def resolve_platforms(self, info):
        return self.gameplatform_set.all()
    
class DLCType(DjangoObjectType):

    class Meta:
        model = DLC

    game = graphene.Field(GameType)

    def resolve_game(self, info):
        return Game.objects.get(id=self.game.id)
    