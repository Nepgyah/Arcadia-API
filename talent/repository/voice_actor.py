from talent.exceptions import TalentNotFound
from talent.models import (
    VoiceActor
)

class VoiceActorRepository:

    @staticmethod
    def get_voice_actor(voice_actor_id):
        try:
            return VoiceActor.objects.get(id=voice_actor_id)
        except VoiceActor.DoesNotExist:
            raise TalentNotFound('Voice actor not found') from None
        
    @staticmethod
    def get_voice_actor_roles(voice_actor: VoiceActor):
        return voice_actor.characters.all()
        