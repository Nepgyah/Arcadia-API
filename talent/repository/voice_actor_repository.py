from django.db.models import prefetch_related_objects

from talent.models import (
    VoiceActor
)

class VoiceActorRepository:

    @staticmethod
    def get_voice_actor_by_id(id):
        try:
            return VoiceActor.objects.prefetch_related('characters').get(id=id)
        except VoiceActor.DoesNotExist:
            return None
        