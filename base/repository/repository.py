from main.exceptions import ArcadiaNotFound
from base.models import Franchise, Genre

class FranchiseRepository:

    @staticmethod
    def get_franchise(franchise_id: int) -> Franchise:
        try:
            return Franchise.objects.get(id=franchise_id)
        except Franchise.DoesNotExist:
            raise ArcadiaNotFound('Franchise not found') from None

    @staticmethod
    def does_franchise_exist(franchise_id: int) -> bool:
        return Franchise.objects.filter(id=franchise_id).exists()
    
class GenreRepository:
    
    @staticmethod
    def get_genre(genre_id: int) -> Genre:
        try:
            return Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist:
            raise ArcadiaNotFound('Genre not found') from None
        
    @staticmethod
    def get_genres(genre_id_list: list[int]) -> list[Genre]:
        return Genre.objects.filter(id__in=genre_id_list)
