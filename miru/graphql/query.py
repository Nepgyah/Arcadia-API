import strawberry
import strawberry_django
from strawberry_django.optimizer import optimize
from main.graphql.types import PaginationResultsType, SortInput, PaginationInput

from miru.models import Anime
from miru.exceptions import MiruNotFoundError
from miru.service import MiruService
from miru.repository import MiruRepository
from .types import AnimeType, AnimeListEntryType, CharacterAppearanceType, AppearanceType

@strawberry.input
class AnimeFilterInput:
    title: str = ""
    type: int = -1
    status: int = -1

@strawberry.type
class SearchAnimeResult:
    results: list[AnimeType]
    pagination: PaginationResultsType | None

@strawberry.type
class UserAnimeListResult:
    user: str
    watching: list[AnimeListEntryType]
    completed: list[AnimeListEntryType]
    plan_to: list[AnimeListEntryType]
    on_hold: list[AnimeListEntryType]

@strawberry.type
class MiruQuery:
    
    @strawberry_django.field
    def anime(self, info: strawberry.Info, pk: int) -> AnimeType:
        qs = Anime.objects.filter(id=pk)
        qs = optimize(qs, info)
        try:
            return qs.get()
        except Anime.DoesNotExist as e:
            raise MiruNotFoundError(
                detail="Cannot find requested anime",
                code="miru_anime_not_found"
            ) from e
    
    @strawberry_django.field
    def animes(
        self,
        filters: AnimeFilterInput | None = None,
        sort: SortInput | None = None,
        pagination: PaginationInput | None = None
    ) -> SearchAnimeResult:
        
        if filters is not None:
            filters = strawberry.asdict(filters)

        if sort is not None:
            sort = strawberry.asdict(sort)

        if pagination is not None:
            pagination = strawberry.asdict(pagination)

        anime, pagination = MiruService.anime.search_anime(
            filters,
            sort,
            pagination
        )
        pagination_result = PaginationResultsType(
            per_page=pagination['per_page'],
            total_pages=pagination['total_pages'],
            total_items=pagination['total_items']
        )
        return SearchAnimeResult(
            results=anime,
            pagination=pagination_result
        )
    
    @strawberry_django.field
    def anime_count(self) -> int:
        return MiruRepository.anime.get_anime_count()

    @strawberry_django.field
    def user_anime_list(self, user_id: int) -> UserAnimeListResult:
        user, anime_list = MiruService.list.get_user_list(user_id)
        return UserAnimeListResult(
            user=user,
            watching=anime_list['watching'],
            completed=anime_list['completed'],
            plan_to=anime_list['plan_to'],
            on_hold=anime_list['on_hold'],
        )
    
    @strawberry_django.field
    def anime_roles(self, voice_actor_id: int) -> list[CharacterAppearanceType]:
        anime_roles = MiruService.character.get_anime_roles(voice_actor_id)
        
        return [
            CharacterAppearanceType(
                character=entry['character'],
                appearances=[
                    AppearanceType(
                        role=appearance['role'],
                        anime=appearance['anime']
                    ) for appearance in entry['appearances']
                ]
            ) for entry in anime_roles
        ]
    