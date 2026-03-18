from talent.models import (
    Character
)

class CharacterRepository:

    @staticmethod
    def get_character_by_id(character_id):
        try:
            return Character.objects.get(id=character_id)
        except Character.DoesNotExist:
            return None