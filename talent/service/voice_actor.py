from talent.repository.voice_actor_repository import VoiceActorRepository
from miru.models import AnimeCharacter
class VoiceActorService:

    @staticmethod
    def get_voice_actor_by_id(id):
        voice_actor = VoiceActorRepository.get_voice_actor_by_id(id)
        characters_details = []
        if voice_actor:
            for character in voice_actor.characters.all():
                characters_details.extend(AnimeCharacter.objects.filter(character=character))

        return voice_actor, characters_details