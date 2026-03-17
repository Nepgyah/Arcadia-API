from base.repository.franchise_repository import FranchiseRepository
from miru.repository.miru_repository import MiruRepository

from asobu.models import Game

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
        
    @staticmethod
    def get_franchise_by_game(id):
        if id == None:
            id = 0
        game = Game.objects.get(id=id)

        if game == None or game.franchise == None:
            return None
        else:
            return FranchiseRepository.get_franchise_by_id(game.franchise.id)