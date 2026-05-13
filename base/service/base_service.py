from base.repository import BaseRepository
from base.models import Franchise, Genre

class FranchiseService:

    @staticmethod
    def get_franchise(pk: int) -> Franchise:
        return BaseRepository.franchise.get_franchise(pk)
    
class GenreService:

    @staticmethod
    def get_genre(pk: int) -> Genre:
        return BaseRepository.genre.get_genre(pk)
    
    @staticmethod
    def get_genres(pk_list: list[int]) -> list[Genre]:
        return BaseRepository.genre.get_genres(pk_list)
    
class BaseService:

    franchise = FranchiseService()
    genre = GenreService()