from talent.models import (
    VoiceActor
)

class VoiceActorRepository:

    @staticmethod
    def get_voice_actor_by_id(va_id):
        try:
            return VoiceActor.objects.prefetch_related('characters').get(id=va_id)
        except VoiceActor.DoesNotExist:
            return None
        