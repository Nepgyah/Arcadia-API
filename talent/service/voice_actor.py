from talent.repository.voice_actor_repository import VoiceActorRepository
from miru.models import AnimeCharacter
from talent.models import VoiceActor
class VoiceActorService:

    @staticmethod
    def get_voice_actor_by_id(id, withCharDetails = False):
        if not withCharDetails:
            voice_actor = VoiceActorRepository.get_voice_actor_by_id(id)
        else:
            voice_actor = VoiceActor.objects.prefetch_related(
                'characters__animecharacter_set__anime'
            ).get(id=id)
            character_details = []

            for character in voice_actor.characters.all():
                for link in character.animecharacter_set.all():
                    character_details.append(link)

            return voice_actor, character_details