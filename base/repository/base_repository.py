from base.models import Franchise, Genre

class FranchiseRepository:

    @staticmethod
    def get_franchise(franchise_id: int) -> Franchise:
        return Franchise.objects.get(id=franchise_id)
    
class GenreRepository:

    @staticmethod
    def get_genre(genre_id: int) -> Genre:
        return Genre.objects.get(id=genre_id)
    
    @staticmethod
    def get_genres(genre_id_list: list[int]) -> list[Genre]:
        return Genre.objects.filter(id__in=genre_id_list)

class BaseRepository:
    
    franchise = FranchiseRepository()
    genre = GenreRepository()