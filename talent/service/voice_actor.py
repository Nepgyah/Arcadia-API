from django.db.models import Prefetch
from asobu.models import GameCharacter
from talent.repository.voice_actor import VoiceActorRepository
from talent.models import VoiceActor, Character
from miru.models.relations import AnimeCharacter

class VoiceActorService:

    @staticmethod
    def get_voice_actor(voice_actor_id: int) -> VoiceActor:
        return VoiceActorRepository.get_voice_actor(voice_actor_id)

    @staticmethod
    def get_voice_actor_roles(voice_actor_id: int):
        voice_actor = VoiceActorRepository.get_voice_actor(voice_actor_id)
        return VoiceActorRepository.get_voice_actor_roles(voice_actor)