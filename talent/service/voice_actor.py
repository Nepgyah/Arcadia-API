from django.db.models import Prefetch
from asobu.models import GameCharacter
from talent.repository.voice_actor_repository import VoiceActorRepository
from talent.models import VoiceActor, Character
from miru.models import AnimeCharacter

class VoiceActorService:

    @staticmethod
    def get_voice_actor_by_id(id, withCharDetails = False):
        if not withCharDetails:
            voice_actor = VoiceActorRepository.get_voice_actor_by_id(id)
            return voice_actor
        else:
            voice_actor = VoiceActor.objects.prefetch_related(
                Prefetch(
                    'characters',
                    queryset=Character.objects.prefetch_related(
                        Prefetch(
                            'animecharacter_set', 
                            queryset=AnimeCharacter.objects.select_related('anime')
                        ),
                        Prefetch(
                            'gamecharacter_set',
                            queryset=GameCharacter.objects.select_related('game')
                        )
                    ),
                )
            ).get(id=id)
            anime_details = []
            game_details = []

            for character in voice_actor.characters.all():
                for animeLink in character.animecharacter_set.all():
                    anime_details.append(animeLink)

                for gameLink in character.gamecharacter_set.all():
                    game_details.append(gameLink)

            character_details = {
                'animes': anime_details,
                'games': game_details
            }

            return voice_actor, character_details