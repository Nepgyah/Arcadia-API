from asobu.models import Game

class AsobuService:

    @staticmethod
    def total_game_count() -> int:
        return Game.objects.all().count()