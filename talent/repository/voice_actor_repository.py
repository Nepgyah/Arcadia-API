from talent.models import (
    VoiceActor
)

class VoiceActorRepository:

    @staticmethod
    def get_voice_actor_by_id(id):
        try:
            return VoiceActor.objects.get(id=id)
        except VoiceActor.DoesNotExist:
            return None
        