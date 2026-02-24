from base.repository.franchise_repository import FranchiseRepository
from miru.repository.miru_repository import MiruRepository

class FranchiseService:

    @staticmethod
    def get_franchise_by_anime(id):
        if id == None:
            id = 0
        anime = MiruRepository.get_anime_by_id(id)
        if anime == None or anime.franchise == None:
            return None
        else:
            return FranchiseRepository.get_franchise_by_id(anime.franchise.id)