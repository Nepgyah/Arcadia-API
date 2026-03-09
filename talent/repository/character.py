from talent.models import (
    Character
)

class CharacterRepository:

    @staticmethod
    def get_character_by_id(id):
        try:
            return Character.objects.get(id=id)
        except Character.DoesNotExist:
            return None