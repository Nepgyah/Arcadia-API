from base.repository import FranchiseRepository, GenreRepository
from base.models import Franchise, Genre

class FranchiseService:

    @staticmethod
    def get_franchise(franchise_id: int) -> Franchise:
        return FranchiseRepository.get_franchise(franchise_id)
    
class GenreService:

    @staticmethod
    def get_genre(genre_id: int) -> Genre:
        return GenreRepository.get_genre(genre_id)
    
    @staticmethod
    def get_genres(genre_id_list: list[int]) -> list[Genre]:
        return GenreRepository.get_genres(genre_id_list)