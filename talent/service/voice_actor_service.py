from talent.repository.voice_actor_repository import VoiceActorRepository

class VoiceActorService:

    @staticmethod
    def get_voice_actor_by_id(id):
        return VoiceActorRepository.get_voice_actor_by_id(id)