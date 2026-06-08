from talent.repository.voice_actor import VoiceActorRepository
from talent.models import VoiceActor
from talent.exceptions import TalentValidationError

class VoiceActorService:

    @staticmethod
    def get_voice_actor(voice_actor_id: int) -> VoiceActor:
        return VoiceActorRepository.get_voice_actor(voice_actor_id)

    @staticmethod
    def get_voice_actor_roles(voice_actor_id: int):
        voice_actor = VoiceActorRepository.get_voice_actor(voice_actor_id)
        return VoiceActorRepository.get_voice_actor_roles(voice_actor)
    
    @staticmethod
    def search_voice_actor(name: str) -> list[VoiceActor]:
        if(len(name) < 3):
            raise TalentValidationError("Query must be greater than 3 characters")
        return VoiceActorRepository.search_voice_actor(name=name)