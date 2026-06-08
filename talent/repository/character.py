from django.db.models import Q
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
        
    @staticmethod
    def get_characters_by_id(character_ids: list, get_va_data = False) -> list:
        if get_va_data is True:
            return Character.objects.filter(id__in=character_ids).prefetch_related(
                'voice_actor'
            )
        
        return Character.objects.filter(id__in=character_ids)
    
    @staticmethod
    def search_characters(name: str) -> list[Character]:
        return Character.objects.filter(
            Q(first_name__contains=name) |
            Q(last_name__contains=name) 
        )