from talent.repository.character import CharacterRepository

class CharacterService:

    @staticmethod
    def get_character_by_id(character_id):
        return CharacterRepository.get_character_by_id(character_id)
    
    @staticmethod
    def get_characters_by_id(character_ids: list, get_va_data = False) -> list:
        """
        Filters and returns character map with ID/Key acccess
        """
        if get_va_data is True:
            characters = CharacterRepository.get_characters_by_id(
                character_ids = character_ids,
                get_va_data=True
            )
        else:
            characters = CharacterRepository.get_characters_by_id(
                character_ids = character_ids,
                get_va_data=False
            )
        return {
            character.id: character for character in characters
        }